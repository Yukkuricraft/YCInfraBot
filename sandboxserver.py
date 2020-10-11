#!/usr/bin/python3
import discord
from discord.ext.commands import Context

import base64
import tempfile
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

import secrets.YCInfraBotSecrets as secrets

ENABLED_CHANNELS = [
    742098922176118885,  # bot-fuckery
    265218973535174657,  # dickaroundwithbot
    731533951889440819,  # how-2-technology
]

gcp_sa_json_b64 = secrets.SA_JSON_KEY_B64.encode("ascii")
gcp_sa_json_bytes = base64.b64decode(gcp_sa_json_b64)
gcp_sa_json_str = gcp_sa_json_bytes.decode("ascii")

# Why? Because https://github.com/apache/libcloud/pull/1214 needs to be merged still
gcp_sa_temp_file = tempfile.NamedTemporaryFile()
gcp_sa_temp_file.write(gcp_sa_json_str.encode())
gcp_sa_temp_file.flush()  # Occasionally getting cases where contents aren't flushed by the time ComputeEngine() is called

ComputeEngine = get_driver(Provider.GCE)
gcp_driver = ComputeEngine(
    secrets.SA_EMAIL,
    gcp_sa_temp_file.name,
    project=secrets.GCP_PROJECT_ID,
    datacenter=secrets.GCP_PROJECT_ZONE,
    auth_type="SA",
)


def getYCNode():
    nodes = gcp_driver.list_nodes(secrets.GCP_PROJECT_ZONE)
    nodes = list(filter(lambda node: node.name == secrets.SANDBOX_COMPUTE_INSTANCE_NAME, nodes))

    if len(nodes) > 1:
        raise Exception("Got more than one node - this should not be possible.")

    return nodes[0]


def isYCNodeRunning():
    node = getYCNode()
    return node.state.upper() == "RUNNING"


async def stopServer(ctx: Context):
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


async def startServer(ctx: Context):
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


async def checkStatusServer(ctx: Context):
    node = getYCNode()
    await ctx.send(f"Server node `{node.name}` is currently: `{node.state.upper()}`")
