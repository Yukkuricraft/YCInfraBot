#!/usr/bin/python3
from __future__ import annotations

import re
import discord
import cleverbot

from typing import Optional
import secrets.YCInfraBotSecrets as secrets


class Cleverbot:
    __instance = None
    __conversations = {}
    __cleverbot = None

    @staticmethod
    def getInstance() -> Cleverbot:
        if Cleverbot.__instance is None:
            Cleverbot()
        return Cleverbot.__instance

    def __init__(self):
        if Cleverbot.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            Cleverbot.__instance = self

        self.__cleverbot = cleverbot.Cleverbot(secrets.CLEVERBOT_API_KEY)

    def getConvoKey(self, user_id: int) -> Optional[str]:
        if user_id in self.__conversations:
            return self.__conversations[user_id]
        else:
            return None

    def storeConvoKey(self, user_id: int, convo_key: str) -> None:
        self.__conversations[user_id] = convo_key

    def formatAndNormalizeMessage(self, msg_content: str) -> str:
        bot_id_str = f"<@!{secrets.DISCORD_BOT_USER_ID}>"

        patterns_to_remove = [
            # TODO: one day make this more robust than what I threw together in 10 minutes
            f"^(?:[Hh]ey,? ?)?{bot_id_str},?",
            f"^(?:[Hh]i,? ?)?{bot_id_str},?",
            f"{bot_id_str}[?!.]? ?$",
        ]

        for regex in patterns_to_remove:
            msg_content = re.sub(regex, "", msg_content)

        patterns_to_replace_with_cleverbot = [f"{bot_id_str}"]

        for regex in patterns_to_replace_with_cleverbot:
            msg_content = re.sub(regex, "cleverbot", msg_content)

        return msg_content

    async def respond(self, msg: discord.Message) -> None:
        sender = msg.author

        cleaned_msg = self.formatAndNormalizeMessage(msg.content)

        convo_key = self.getConvoKey(sender)
        if convo_key is None:
            convo = self.__cleverbot.conversation()
            resp = convo.say(cleaned_msg)
            self.storeConvoKey(sender, convo.cs)
        else:
            resp = self.__cleverbot.say(cleaned_msg, cs=convo_key)

        await msg.channel.send(resp)


async def respond(msg: discord.Message) -> None:
    cb = Cleverbot.getInstance()
    await cb.respond(msg)
