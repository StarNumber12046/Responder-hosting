import discord
from discord.ext import commands
import json
import os
def get_prefix(bot, message):

  if message.guild is None:
    prefix = commands.when_mentioned_or("e? ", "e?")(bot, message)

  else:
    with open("data/prefixes.json", "r") as f:
      json_prefixes = json.load(f)

    try:
      oof = str(json_prefixes[str(message.guild.id)])
      prefix = commands.when_mentioned_or(f"{oof} ", oof)(bot, message)

    except KeyError:
      prefix = commands.when_mentioned_or("r. ", "r-")(bot, message)

  return prefix
responder = commands.Bot(command_prefix=get_prefix)
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    responder.load_extension(f'cogs.{filename[:-3]}')
responder.run('NzI1MzQyMTQ4NDg4MDY5MTYw.XvNVhA.pr4oTJGyDpsMuNM-0ZjeLl2D1FI')
