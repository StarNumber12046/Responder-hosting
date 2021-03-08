import discord
import os
from discord.ext import commands
import jishaku
import prefix
import dotenv as envfiles
import server

bot = commands.Bot(command_prefix=prefix.get_prefix, intents=discord.Intents.all())
print(discord)
bot.remove_command('help')
bot.load_extension('jishaku')

@bot.event
async def on_ready():
    print('Online come', bot.user)

for a in os.listdir("./cogs"):
    if a.endswith(".py"):
        if a == 'notload.py':
            pass
        else:
            bot.load_extension(f"cogs.{a[:-3]}")
envfiles.load_dotenv(dotenv_path='.env')
server.keep_alive()
bot.run(os.environ.get('token'))
