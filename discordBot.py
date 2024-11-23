import requests

from database import getFormId
from config import DISCORD_LETTERLOOP_WEBHOOK


def sendDiscordMessage(message):
    requests.post(DISCORD_LETTERLOOP_WEBHOOK, json={"content": message})


def createFormMessage():
    formId = getFormId()
    message = f"New FredderLoop issue just dropped! 3 weeks to add questions here: https://docs.google.com/forms/d/{formId}/edit "
    message += "\nAlso, don't forget to set edit responses to true... google form api currently doesn't support setting it in code"
    sendDiscordMessage(message)


def collectResponsesMessage():
    formId = getFormId()
    message = (
        f"Ready for responses here: https://docs.google.com/forms/d/{formId}/viewform"
    )
    sendDiscordMessage(message)


def shareResponsesMessage(doc_id: str):
    message = f"FredderLoop issue over! View responses here: https://docs.google.com/document/d/{doc_id}/edit"
    sendDiscordMessage(message)
