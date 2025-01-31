# docs documentation: https://googleapis.github.io/google-api-python-client/docs/dyn/drive_v3.html

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
        print(f"adding: {email}")
        drive_service.permissions().create(
            fileId=file_id,
            body={"type": "user", "emailAddress": email, "role": permission},
        ).execute()
        print(f"added {permission} role for: {email}")


# https://developers.google.com/drive/api/guides/manage-sharing#python
def _transfer_ownership(
    drive_service, file_id: str, permission_id: str, email: str
) -> None:
    # https://issuetracker.google.com/issues/228791253
    print(
        "Currently Drive does not support changing the ownership for items which are owned by gmail.com accounts; it's supported for Workspace accounts."
    )


def get_permissions(drive_service, file_id: str) -> dict:
    permissions = (
        drive_service.permissions().list(fileId=file_id).execute()["permissions"]
    )
    print(permissions)
    return permissions


def trash_document(drive_service, file_id: str) -> None:
    print(f"Trashing document: {file_id}")
    body = {"trashed": True}
    drive_service.files().update(fileId=file_id, body=body).execute()


def untrash_file(drive_service, file_id: str) -> None:
    print(f"Attempting to untrash file: {file_id}")
    body = {"trashed": False}
    drive_service.files().update(fileId=file_id, body=body).execute()


def add_anyone_write(drive_service, file_id: str) -> None:
    print(f"Adding anyoneWithLink can write permission: {file_id}")
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
    print(f"Moving {file_id} from {previous_parents} to {folder_id}")

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
