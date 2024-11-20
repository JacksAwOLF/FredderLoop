import requests

from database import getFormId
from config import DISCORD_LETTERLOOP_WEBHOOK


def sendDiscordMessage(message):
    requests.post(DISCORD_LETTERLOOP_WEBHOOK, json={"content": message})


def createFormMessage():
    formId = getFormId()
    message = f"New FredderLoop issue just dropped! 3 weeks (until the 21st) to add questions here: https://docs.google.com/forms/d/{formId}/edit "
    message += "\nAlso, don't forget to set edit responses to true... google form api currently doesn't support setting it in code"
    sendDiscordMessage(message)


def addQuestionsReminderMessage():
    formId = getFormId()
    message = (
        f"Last day to add questions! https://docs.google.com/forms/d/{formId}/edit"
    )
    sendDiscordMessage(message)


def collectResponsesMessage():
    formId = getFormId()
    message = (
        f"Ready for responses here. Due in a week (the 28th): https://docs.google.com/forms/d/{formId}/viewform"
    )
    sendDiscordMessage(message)


def submissionReminderMessage():
    formId = getFormId()
    message = f"Last day to submit your answers (there is NO auto-submit)! https://docs.google.com/forms/d/{formId}/viewform"
    sendDiscordMessage(message)


def lastHourReminderMessage():
    formId = getFormId()
    message = f"Only ONE MORE HOUR to submit your answers (there is NO auto-submit)! https://docs.google.com/forms/d/{formId}/viewform"
    sendDiscordMessage(message)


def shareResponsesMessage(doc_id: str):
    message = f"FredderLoop issue over! View responses here: https://docs.google.com/document/d/{doc_id}/edit"
    sendDiscordMessage(message)
