import constants
import driveUtil
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

    form = form_service.forms().get(formId=formId).execute()
    responses = form_service.forms().responses().list(formId=formId).execute()

    # if nobody submitted a response, do nothing
    if "responses" not in responses or len(responses["responses"]) == 0:
        sendDiscordMessage("Nobody submitted a response this month :(")
        exit()

    responses = responses["responses"]
    print("responses", responses)

    try:
        doc_id, email_mapping = createNewsletter(form=form, responses=responses)
        emails = []
        need_to_add = []
        for email in email_mapping.keys():
            if "N/A-" in email and "@" not in email:
                need_to_add.append(email_mapping[email])
            else:
                emails.append(email)
        print(f"emails found: {emails}")
        print(f"email not found, need to share newsletter with: {need_to_add}")
        
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
        print(f"create newsletter failed:\n{e}")

        for response in responses:
            if "respondentEmail" in response:
                drive_service.permissions().create(
                    fileId=formId, body={"type": "user", "emailAddress": response["respondentEmail"], "role": "writer"}
                ).execute()

                print("sharing form with", response["respondentEmail"])
        shareResponsesMessage(formId, [])
