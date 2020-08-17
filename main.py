#!/usr/bin/python3

import discord
from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

import base64
import json
import tempfile
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

import utils
import cbwrapper as cb
import sandboxserver as sandbox
import secrets.YCInfraBotSecrets as secrets

# discord.py
PREFIX = "!"
bot = commands.Bot(command_prefix=PREFIX)


@bot.command(name="ycsandbox")
async def _ycsandbox(ctx: Context, *args):
    usage = f"Usage: `{PREFIX}ycsandbox [start|stop|status]`"

    if not args or len(args) > 1:
        await ctx.send(usage)
        return

    subcmd = args[0]
    try:
        if subcmd in ["stop", "suspend"]:
            await sandbox.stopServer(ctx)
        elif subcmd in ["start", "resume"]:
            await sandbox.startServer(ctx)
        elif subcmd == "status":
            await sandbox.checkStatusServer(ctx)
        else:
            await ctx.send(usage)
    except Exception as e:
        await ctx.send(f"An error occurred while processing your command: {e}")


DISCORD_HELP_MESSAGE = """
```
YCRemiBot
-------
A bot mostly for admins. And a chat bot.

CHAT BOT:
The bot will respond to one of two situations:
    - Your message contains a mention for @YCRemiBot
        Eg, "Hey @YCRemiBot. How are you?"
    - Your message starts with a special prefix, the double semicolon (;;), to denote it is a chatbot message.
        Eg, ";;Your face smells like diaperheads"

ADMIN COMMANDS:
  !ycsandbox status
    - Get the status of the sandbox
  !ycsandbox [start|resume]
    - Starts the sandbox
  !ycsandbox [stop|suspend]
    - Stops the sandbox
```
"""


@bot.event
async def on_message(message: Message):
    # Event is the bot's own message. Ignore.
    if message.author == bot.user:
        return

    # Help message
    if message.content == utils.getBotIdString():
        # TODO: This is hacky. Make real help handler
        await message.channel.send(DISCORD_HELP_MESSAGE)
        return

    # If event has mentions, check if the mention is the bot
    for mention in message.mentions:
        if str(mention.id) == str(secrets.DISCORD_BOT_USER_ID):
            await cb.respond(message)
    # Alternatively watch for special prefix to denote "chatbot message"
    if message.content[:2] == ";;":
        # TODO: make this more robust
        await cb.respond(message)

    # @bot.event takes precedence in capturing the event.
    # Use .process_commands() to process all bot.command cmds.
    await bot.process_commands(message)


# Start bot
token = secrets.DISCORD_BOT_TOKEN
print("Bot starting")
bot.run(token)
