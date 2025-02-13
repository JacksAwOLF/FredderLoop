import constants
import driveUtil
import formUtil
import masker
from createNewsletter import createNewsletter
from config import NEWSLETTER_FOLDER_ID
from database import getFormId
from discordBot import shareResponsesMessage, sendDiscordMessage
from services import create_service

if __name__ == "__main__":
    form_service = create_service(constants.FORMS_SERVICE)
    drive_service = create_service(constants.DRIVE_SERVICE)

    formId = getFormId()
    if formId == "":
        exit()

    form = formUtil.get_form(form_service=form_service, form_id=formId)
    responses = formUtil.get_form_responses(form_service=form_service, form_id=formId)

    # if nobody submitted a response, do nothing
    if "responses" not in responses or len(responses["responses"]) == 0:
        sendDiscordMessage("Nobody submitted a response this month :(")
        exit()

    responses = responses["responses"]

    try:
        doc_id, email_mapping = createNewsletter(form=form, responses=responses)
        emails = []
        need_to_add = []
        for email in email_mapping.keys():
            if "N/A-" in email and "@" not in email:
                need_to_add.append(email_mapping[email])
            else:
                emails.append(email)
        masker.log(f"Number of emails found: {len(emails)}")
        masker.log(
            f"Email(s) not found, need to share newsletter with {len(need_to_add)} users"
        )

        # Move from root to Newsletter folder
        driveUtil.move_file_to_folder(
            drive_service=drive_service, file_id=doc_id, folder_id=NEWSLETTER_FOLDER_ID
        )

        driveUtil.share_document(
            drive_service=drive_service,
            file_id=doc_id,
            emails=emails,
            permission=driveUtil.COMMENT_PERMISSION,
        )
        shareResponsesMessage(doc_id, need_to_add)
    except Exception as e:
        masker.log(f"create newsletter failed:\n{e}")

        for response in responses:
            if "respondentEmail" in response:
                drive_service.permissions().create(
                    fileId=formId,
                    body={
                        "type": "user",
                        "emailAddress": response["respondentEmail"],
                        "role": "writer",
                    },
                ).execute()

                masker.log(f"sharing form with {response['respondentEmail'][0:3]}******")
        shareResponsesMessage(formId, [])
