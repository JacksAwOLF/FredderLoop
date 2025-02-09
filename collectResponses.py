import constants as c
import driveUtil
import services as svc
from database import getFormId
from discordBot import collectResponsesMessage

if __name__ == "__main__":
    drive_service = svc.create_service(c.DRIVE_SERVICE)

    formId = getFormId()
    if formId == "":
        exit()

    # remove all permissions (other than owning the file itself)
    driveUtil.remove_all_permissions(drive_service=drive_service, file_id=formId)

    # add permission to view the files to anyone for submission
    driveUtil.add_anyone_read(drive_service=drive_service, file_id=formId)

    collectResponsesMessage()
