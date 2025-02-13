# docs documentation: https://googleapis.github.io/google-api-python-client/docs/dyn/drive_v3.html

import masker

# constants
WRITER_PERMISSION = "writer"
COMMENT_PERMISSION = "commenter"
valid_permissions = [WRITER_PERMISSION, COMMENT_PERMISSION]


def share_document(drive_service, file_id: str, emails: list, permission: str) -> None:
    if permission not in valid_permissions:
        raise TypeError(f"unknown permission type: {permission}")
    if type(emails) != list:
        raise TypeError(f"incorrect emails type: {type(emails)}")
    for email in emails:
        masker.log(f"adding: {email[0:3]}******")
        drive_service.permissions().create(
            fileId=file_id,
            body={"type": "user", "emailAddress": email, "role": permission},
        ).execute()
        masker.log(f"added {permission} role for: {email[0:3]}******")


# https://developers.google.com/drive/api/guides/manage-sharing#python
def _transfer_ownership(
    drive_service, file_id: str, permission_id: str, email: str
) -> None:
    # https://issuetracker.google.com/issues/228791253
    masker.log(
        "Currently Drive does not support changing the ownership for items which are owned by gmail.com accounts; it's supported for Workspace accounts."
    )


def add_anyone_read(drive_service, file_id: str) -> None:
    drive_service.permissions().create(
        fileId=file_id, body={"type": "anyone", "role": "reader"}
    ).execute()


def add_anyone_write(drive_service, file_id: str) -> None:
    drive_service.permissions().create(
        fileId=file_id,
        body={
            "type": "anyone",
            "role": "writer",
        },
    ).execute()


def add_write_permission(drive_service, file_id: str, email: str) -> None:
    drive_service.permissions().create(
        fileId=file_id,
        body={
            "type": "user",
            "emailAddress": email,
            "role": "writer",
        },
    ).execute()


def get_permissions(drive_service, file_id: str) -> dict:
    permissions = (
        drive_service.permissions().list(fileId=file_id).execute()["permissions"]
    )
    return permissions


def remove_all_permissions(drive_service, file_id: str) -> None:
    num_permissions_removed = 0
    result = (
        drive_service.permissions()
        .list(
            fileId=file_id,
        )
        .execute()
    )
    for permission in result["permissions"]:
        if permission["role"] != "owner":
            drive_service.permissions().delete(
                fileId=file_id, permissionId=permission["id"]
            ).execute()
            num_permissions_removed += 1

    masker.log(f"Removed {num_permissions_removed} non-owner permissions")


def trash_document(drive_service, file_id: str) -> None:
    masker.log(f"Trashing document: {file_id[0:3]}******")
    body = {"trashed": True}
    drive_service.files().update(fileId=file_id, body=body).execute()


def untrash_file(drive_service, file_id: str) -> None:
    masker.log(f"Attempting to untrash file: {file_id[0:3]}******")
    body = {"trashed": False}
    drive_service.files().update(fileId=file_id, body=body).execute()


def add_anyone_write(drive_service, file_id: str) -> None:
    masker.log(f"Adding anyoneWithLink can write permission: {file_id[0:3]}******")
    body = {
        "type": "anyone",
        "role": "writer",
        "allowFileDiscovery": False,
    }
    drive_service.permissions().create(fileId=file_id, body=body).execute()


def move_file_to_folder(drive_service, file_id: str, folder_id: str) -> str:
    # Retrieve the existing parents to remove
    file = drive_service.files().get(fileId=file_id, fields="parents").execute()
    previous_parents = ",".join(file.get("parents"))
    masker.log(
        f"Moving {file_id[0:3]}****** from {previous_parents[0:3]}****** to {folder_id[0:3]}******"
    )

    # Move the file to the new folder
    file = (
        drive_service.files()
        .update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields="id, parents",
        )
        .execute()
    )

    return file.get("parents")


def list_files(drive_service, query: str = None) -> dict:
    return drive_service.files().list(q=query).execute()


def search_files_by_name(drive_service, name: str, query: str = None) -> dict:
    results = {}
    all_files = list_files(drive_service=drive_service, query=query)
    for file in all_files["files"]:
        if name in file["name"]:
            results[file["id"]] = file["name"]
    return results


def list_files_in_folder(drive_service, folder_id: str) -> dict:
    query = f"parents in '{folder_id}'"
    return drive_service.files().list(q=query).execute()


def list_folders(drive_service) -> dict:
    query = "mimeType='application/vnd.google-apps.folder'"
    return drive_service.files().list(q=query).execute()


def list_drives(drive_service) -> dict:
    return drive_service.drives().list().execute()


def list_file_labels(drive_service, file_id: str) -> dict:
    return drive_service.files().listLabels(fileId=file_id).execute()


def get_file(drive_service, file_id: str) -> dict:
    return drive_service.files().get(fileId=file_id, fields="*").execute()
