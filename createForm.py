import constants
import driveUtil
from config import GOOGLE_DRIVE_FOLDER_ID
from defaultForm import getDefaultFormHead, defaultFormBody
from discordBot import createFormMessage
from database import saveFormId
from services import create_service


if __name__ == "__main__":
    form_service = create_service(constants.FORMS_SERVICE)
    drive_service = create_service(constants.DRIVE_SERVICE)

    # create the form
    form = form_service.forms().create(body=getDefaultFormHead()).execute()
    formId = form["formId"]

    # add default questions
    form_service.forms().batchUpdate(formId=formId, body=defaultFormBody).execute()

    # set form editing permissions to anyone with the link
    drive_service.permissions().create(
        fileId=formId,
        body={
            "type": "anyone",
            "role": "writer",
        },
    ).execute()

    # Move the form to specific folderId
    driveUtil.move_file_to_folder(
        drive_service=drive_service, file_id=formId, folder_id=GOOGLE_DRIVE_FOLDER_ID
    )

    # save formId in database
    print("form created: ", form)
    saveFormId(form["formId"])

    createFormMessage()
