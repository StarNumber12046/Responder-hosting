import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='r-' or 'r.')
print(discord)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Online come', bot.user)

for a in os.listdir("./cogs"):
    if a.endswith(".py"):
        if a == 'notload.py':
            pass
        else:
            bot.load_extension(f"cogs.{a[:-3]}")
bot.run('NzI1MzQyMTQ4NDg4MDY5MTYw.XvNVhA.pr4oTJGyDpsMuNM-0ZjeLl2D1FI')
