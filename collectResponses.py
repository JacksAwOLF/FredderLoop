import constants as c
import services as svc
from database import getFormId
from discordBot import collectResponsesMessage

if __name__ == "__main__":
    drive_service = svc.create_service(c.DRIVE_SERVICE)

    formId = getFormId()
    if formId == "":
        exit()

    # remove all permissions (other than owning the file itself)
    result = (
        drive_service.permissions()
        .list(
            fileId=formId,
        )
        .execute()
    )

    for permission in result["permissions"]:
        if permission["role"] != "owner":
            drive_service.permissions().delete(
                fileId=formId, permissionId=permission["id"]
            ).execute()

            print("removing", permission)

    # add permission to view the files to anyone for submission
    drive_service.permissions().create(
        fileId=formId, body={"type": "anyone", "role": "reader"}
    ).execute()

    collectResponsesMessage()
