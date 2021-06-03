import discord
from discord.ext import commands
import json
import os
def get_prefix(bot, message):
  with open("data/settings.json", "r") as f:
    settings = json.load(f)
    f.close()

  if message.guild is None:
    prefix = commands.when_mentioned_or(settings["default-prefix"])(bot, message)

  else:
    with open("data/prefixes.json", "r") as f:
      json_prefixes = json.load(f)
      f.close()

    try:
      oof = str(json_prefixes[str(message.guild.id)])
      prefix = commands.when_mentioned_or(f"{oof} ", oof)(bot, message)

    except KeyError:
      prefix = commands.when_mentioned_or(settings["default-prefix"])(bot, message)

  return prefix


