import requests
import os

from database import getFormId
from config import DISCORD_LETTERLOOP_WEBHOOK


def sendDiscordMessage(message: str) -> None:
    if "FREDDERLOOP_PROD" in os.environ:
        requests.post(DISCORD_LETTERLOOP_WEBHOOK, json={"content": message})
    else:
        print(f"Discord message testing:\n{message}")


def createFormMessage() -> None:
    formId = getFormId()
    message = (
        f"New FredderLoop issue just dropped! 3 weeks (21th 00:00) to add questions here: https://docs.google.com/forms/d/{formId}/edit"
        + "\n\nAlso, don't forget to set edit responses to true... google form api currently doesn't support setting it in code"
    )
    sendDiscordMessage(message)


def addQuestionsReminderMessage() -> None:
    formId = getFormId()
    message = f"Last day to add questions (due end of day)! https://docs.google.com/forms/d/{formId}/edit"
    sendDiscordMessage(message)


def collectResponsesMessage():
    formId = getFormId()
    message = (
        f"Ready for responses here. Due in a week (28th 00:00): https://docs.google.com/forms/d/{formId}/viewform"
        + "\n\n*Reminder: You'll only be able to see the newsletter if you submit a response*"
    )
    sendDiscordMessage(message)


def submissionReminderMessage():
    formId = getFormId()
    message = f"Last day to submit your answers, due end of day (there is NO auto-submit)! https://docs.google.com/forms/d/{formId}/viewform"
    sendDiscordMessage(message)


def lastHourReminderMessage():
    formId = getFormId()
    message = f"Only ONE MORE HOUR to submit your answers (there is NO auto-submit)! https://docs.google.com/forms/d/{formId}/viewform"
    sendDiscordMessage(message)


def shareResponsesMessage(doc_id: str):
    message = (
        "FredderLoop issue over!"
        + "\nNew FredderLoop starts on the 1st!"
        + "\n"
        + f"\nView newsletter here: https://docs.google.com/document/d/{doc_id}/edit"
    )
    sendDiscordMessage(message)
