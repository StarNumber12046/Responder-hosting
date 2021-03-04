import discord
from discord.ext import commands
import json
import os
def get_prefix(bot, message):

  if message.guild is None:
    prefix = commands.when_mentioned_or("r- ", "r-")(bot, message)

  else:
    with open("data/prefixes.json", "r") as f:
      json_prefixes = json.load(f)

    try:
      oof = str(json_prefixes[str(message.guild.id)])
      prefix = commands.when_mentioned_or(f"{oof} ", oof)(bot, message)

    except KeyError:
      prefix = commands.when_mentioned_or("r. ", "r-")(bot, message)

  return prefix


