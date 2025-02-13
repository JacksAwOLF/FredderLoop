import constants
import driveUtil
import formUtil
import masker
from config import GOOGLE_DRIVE_FOLDER_ID
from discordBot import createFormMessage
from database import saveFormId
from services import create_service


if __name__ == "__main__":
    form_service = create_service(constants.FORMS_SERVICE)
    drive_service = create_service(constants.DRIVE_SERVICE)

    # create the form
    form = formUtil.create_form(form_service=form_service)
    formId = form["formId"]

    # add default questions
    formUtil.add_default_form_body()

    # set form editing permissions to anyone with the link
    driveUtil.add_anyone_write(drive_service=drive_service, file_id=formId)

    # Move the form to specific folderId
    driveUtil.move_file_to_folder(
        drive_service=drive_service, file_id=formId, folder_id=GOOGLE_DRIVE_FOLDER_ID
    )

    # save formId in database
    masker.log(f"form created: {formId[0:3]}********")
    saveFormId(form["formId"])

    createFormMessage()
