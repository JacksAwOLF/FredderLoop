import discord
import requests

from database import getFormId
from config import DISCORD_LETTERLOOP_CHANNELID, BOT_TOKEN, DISCORD_LETTERLOOP_WEBHOOK


def sendDiscordMessage(message):
    # client = discord.Client(intents=discord.Intents.default())

    # @client.event
    # async def on_ready():
    #     channel = client.get_channel(DISCORD_LETTERLOOP_CHANNELID)
    #     if channel:
    #         await channel.send(message)
    #     await client.close()
    # client.run(BOT_TOKEN)
    requests.post(DISCORD_LETTERLOOP_WEBHOOK, json={"content": message})


sendDiscordMessage("hi")


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


def shareResponsesMessage():
    formId = getFormId()
    message = f"FredderLoop issue over! View responses here: https://docs.google.com/forms/d/{formId}/edit#responses"
    sendDiscordMessage(message)
