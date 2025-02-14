"""Start Fredderloop by creating form"""

from datetime import datetime

from src import config
from src.utils import database, discord, drive, forms, masker, services


if __name__ == "__main__":
    docs_service = services.create_docs_service()
    drive_service = services.create_drive_service()
    form_service = services.create_forms_service()

    # create the form
    masker.log("creating form")
    date = datetime.today().strftime("%Y-%m-%d")
    form = forms.create_form(form_service=form_service, date=date)
    # Key must be "formID"
    form_id = form["formId"]
    # save form_id in database
    masker.log(f"form created: {form_id[0:3]}********")
    database.save_form_id(docs_service=docs_service, form_id=form_id)
    database.push_to_database(docs_service=docs_service, content=f"formTitle:{date}")

    # add default questions
    masker.log("add default questions")
    forms.add_default_form_body(form_service=form_service, form_id=form_id)

    # set form editing permissions to anyone with the link
    masker.log("add editing permissions")
    drive.add_anyone_write(drive_service=drive_service, file_id=form_id)

    # Move the form to specific folderId
    masker.log("moving folder")
    drive.move_file_to_folder(
        drive_service=drive_service,
        file_id=form_id,
        folder_id=config.GOOGLE_DRIVE_FOLDER_ID,
    )

    discord.create_form_message()
