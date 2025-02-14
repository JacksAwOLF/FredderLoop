"""Create newsletter and share responses"""

import sys

from src import config
from src.helpers import create_newsletter
from src.utils import database, discord, drive, forms, masker, services

if __name__ == "__main__":
    docs_service = services.create_docs_service()
    drive_service = services.create_drive_service()
    form_service = services.create_forms_service()

    form_id = database.get_form_id(docs_service=docs_service)
    if form_id == "":
        masker.log("no form id found")
        sys.exit()

    form = forms.get_form(form_service=form_service, form_id=form_id)
    responses = forms.get_form_responses(form_service=form_service, form_id=form_id)

    # if nobody submitted a response, do nothing
    if "responses" not in responses or len(responses["responses"]) == 0:
        discord.send_discord_message("Nobody submitted a response this month :(")
        sys.exit()

    responses = responses["responses"]

    try:
        doc_id, email_mapping = create_newsletter.create_newsletter(form=form, responses=responses)
        emails = []
        need_to_add = []
        for email, mapped_email in email_mapping.items():
            if "N/A-" in email and "@" not in email:
                need_to_add.append(mapped_email)
            else:
                emails.append(email)
        masker.log(f"Number of emails found: {len(emails)}")
        masker.log(
            f"Email(s) not found, need to share newsletter with {len(need_to_add)} users"
        )

        # Move from root to Newsletter folder
        drive.move_file_to_folder(
            drive_service=drive_service,
            file_id=doc_id,
            folder_id=config.NEWSLETTER_FOLDER_ID,
        )

        drive.share_document(
            drive_service=drive_service,
            file_id=doc_id,
            emails=emails,
            permission=drive.COMMENT_PERMISSION,
        )
        discord.share_responses_message(doc_id, need_to_add)
    except Exception as e:
        masker.log(f"create newsletter failed:\n{e}")

        for response in responses:
            if "respondentEmail" in response:
                drive_service.permissions().create(
                    fileId=form_id,
                    body={
                        "type": "user",
                        "emailAddress": response["respondentEmail"],
                        "role": "writer",
                    },
                ).execute()

                masker.log(
                    f"sharing form with {response['respondentEmail'][0:3]}******"
                )
        discord.share_responses_message(form_id, [])
