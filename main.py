#!/usr/bin/python3

import discord
from discord.ext import commands

import base64
import json
import tempfile
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

import secrets.YCInfraBotSecrets as secrets

# gcloud/gcp
b64_bytes = secrets.SA_JSON_KEY_B64.encode("ascii")
message_bytes = base64.b64decode(b64_bytes)
gcp_sa_json_str = message_bytes.decode("ascii")

# Why? Because https://github.com/apache/libcloud/pull/1214 needs to be merged still
gcp_sa_temp_file = tempfile.NamedTemporaryFile()
gcp_sa_temp_file.write(gcp_sa_json_str.encode())
gcp_sa_temp_file.flush() # Occasionally getting cases where contents aren't flushed by the time ComputeEngine() is called

ComputeEngine = get_driver(Provider.GCE)
gcp_driver = ComputeEngine(
    secrets.SA_EMAIL,
    key=gcp_sa_temp_file.name,
    project=secrets.GCP_PROJECT_ID,
    auth_typoe="GCE",
)

# discord.py
PREFIX = "!"
bot = commands.Bot(command_prefix=PREFIX)

# bot commands
USAGE = f"Usage: `{PREFIX}ycsandbox [start|stop|status]`"

@bot.command(name="ycsandbox")
async def _ycsandbox(ctx, *args):
    if not args or len(args) > 1:
        await ctx.send(USAGE)
        return

    subcmd = args[0]
    try:
        if subcmd in ["stop", "suspend"]:
            await stopServer(ctx)
        elif subcmd in ["start", "resume"]:
            await startServer(ctx)
        elif subcmd == "status":
            await checkStatusServer(ctx)
        else:
            await ctx.send(USAGE)
    except Exception as e:
        await ctx.send(f"An error occurred while processing your command: {e}")

def getYCNode():
    nodes = gcp_driver.list_nodes(secrets.GCP_PROJECT_ZONE)
    nodes = list(filter(lambda node: node.name == secrets.COMPUTE_INSTANCE_NAME, nodes))

    if len(nodes) > 1:
        raise Exception("Got more than one node - this should not be possible.")

    return nodes[0]

def isYCNodeRunning():
    node = getYCNode()
    return node.state.upper() == "RUNNING"

async def stopServer(ctx):
    if not isYCNodeRunning():
        await ctx.send("Server is not running.")
        return

    await ctx.send("Stopping server... (This may take a minute)")
    node = getYCNode()

    try:
        gcp_driver.suspend_node(node)
        await ctx.send("Stopped server.")
    except Exception as e:
        await ctx.send("Failed to stop server.")
        raise

async def startServer(ctx):
    if isYCNodeRunning():
        await ctx.send("Server is already running.")
        return

    await ctx.send("Starting server...")
    node = getYCNode()

    try:
        gcp_driver.resume_node(node)
        await ctx.send("Started server.")
    except Exception as e:
        await ctx.send("Failed to start server.")
        raise

async def checkStatusServer(ctx):
    node = getYCNode()
    await ctx.send(f"Server node `{node.name}` is currently: `{node.state.upper()}`")


# Start bot
token = secrets.discord_bot_token
print("Bot starting")
bot.run(token)

