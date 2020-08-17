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


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    for mention in message.mentions:
        if str(mention.id) == str(secrets.DISCORD_BOT_USER_ID):
            await cb.respond(message)

    # @bot.event takes precedence in capturing the event.
    # Use .process_commands() to process all bot.command cmds.
    await bot.process_commands(message)

# Start bot
token = secrets.DISCORD_BOT_TOKEN
print("Bot starting")
bot.run(token)
