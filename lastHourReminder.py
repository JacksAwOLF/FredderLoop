import constants
import formUtil
from database import getFormId
from services import create_service
from discordBot import lastHourReminderMessage

if __name__ == "__main__":
    form_service = create_service(constants.FORMS_SERVICE)

    formId = getFormId()
    if formId == "":
        exit()

    form = formUtil.get_form(form_service=form_service, form_id=formId)
    nameQuestionId = form["items"][0]["questionItem"]["question"]["questionId"]

    responses = formUtil.get_form_responses(form_service=form_service, formId=formId)
    names = map(
        lambda x: x["answers"][nameQuestionId]["textAnswers"]["answers"][0]["value"],
        responses["responses"],
    )

    lastHourReminderMessage(list(names))
