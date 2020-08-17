#!/usr/bin/python3
import secrets.YCInfraBotSecrets as secrets


def getBotIdString():
    return f"<@!{secrets.DISCORD_BOT_USER_ID}>"
