import sys

import constants
import driveUtil
from createNewsletter import createNewsletter
from database import getFormId
from discordBot import shareResponsesMessage, sendDiscordMessage
from services import create_service

if __name__ == "__main__":
    production = False  # fail to dev mode
    if len(sys.argv) > 1:
        # check if "production"
        if sys.argv[1] == "production":
            production = True

    form_service = create_service(constants.FORMS_SERVICE)
    drive_service = create_service(constants.DRIVE_SERVICE)

    formId = getFormId()
    if formId == "":
        exit()

    form = (
        form_service.forms()
        .get(formId="1MfEowHxVJtuRVN2IvSu74p_4fK3KwbWcvXeUQg9Vp9E")
        .execute()
    )
    responses = form_service.forms().responses().list(formId=formId).execute()

    # if nobody submitted a response, do nothing
    if "responses" not in responses or len(responses["responses"]) == 0:
        sendDiscordMessage("Nobody submitted a response this month :(")
        exit()

    responses = responses["responses"]
    print("responses", responses)

    doc_id, emails = createNewsletter(form=form, responses=responses)
    driveUtil.share_document(drive_service=drive_service, file_id=doc_id, emails=emails)

    shareResponsesMessage(doc_id, production)
