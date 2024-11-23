import requests

from database import getFormId
from config import DISCORD_LETTERLOOP_WEBHOOK, DISCORD_LETTERLOOP_DEV_WEBHOOK


def sendDiscordMessage(message: str, production: bool) -> None:
    url = DISCORD_LETTERLOOP_DEV_WEBHOOK
    if production:
        url = DISCORD_LETTERLOOP_WEBHOOK
    requests.post(url, json={"content": message})


def createFormMessage(production: bool) -> None:
    formId = getFormId()
    message = (
        f"New FredderLoop issue just dropped! 3 weeks (21th 00:00) to add questions here: https://docs.google.com/forms/d/{formId}/edit"
        + "\n\nAlso, don't forget to set edit responses to true... google form api currently doesn't support setting it in code"
    )
    sendDiscordMessage(message, production)


def addQuestionsReminderMessage(production: bool) -> None:
    formId = getFormId()
    message = f"Last day to add questions (due end of day)! https://docs.google.com/forms/d/{formId}/edit"
    sendDiscordMessage(message, production)


def collectResponsesMessage(production: bool):
    formId = getFormId()
    message = f"Ready for responses here. Due in a week (28th 00:00): https://docs.google.com/forms/d/{formId}/viewform"
    +"\n\n*Reminder: You'll only be able to see the newsletter if you submit a response*"
    sendDiscordMessage(message, production)


def submissionReminderMessage(production: bool):
    formId = getFormId()
    message = f"Last day to submit your answers, due end of day (there is NO auto-submit)! https://docs.google.com/forms/d/{formId}/viewform"
    sendDiscordMessage(message, production)


def lastHourReminderMessage(production: bool):
    formId = getFormId()
    message = f"Only ONE MORE HOUR to submit your answers (there is NO auto-submit)! https://docs.google.com/forms/d/{formId}/viewform"
    sendDiscordMessage(message, production)


def shareResponsesMessage(doc_id: str, production: bool):
    message = (
        "FredderLoop issue over!"
        + "\nNew FredderLoop starts on the 1st!"
        + "\n"
        + f"\nView newsletter here: https://docs.google.com/document/d/{doc_id}/edit"
    )
    sendDiscordMessage(message, production)
