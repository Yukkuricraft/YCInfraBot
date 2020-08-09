#!/usr/bin/python3

import discord
import googleapiclient
import base64

import secrets.YCInfraBotSecrets as secrets

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$remibot"):
        await message.channel.send("Boop")

b64_bytes = secrets.service_account_key_b64.encode("ascii")
message_bytes = base64.b64decode(b64_bytes)
gcp_sa_json = message_bytes.decode("ascii")

token = secrets.discord_bot_token
print(token)
client.run(token)

