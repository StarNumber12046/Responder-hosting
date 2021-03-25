import discord
import os
from discord.ext import commands
import jishaku
import prefix
import dotenv as envfiles
import server
from discord_slash import SlashCommand

bot = commands.Bot(command_prefix=prefix.get_prefix, intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True) # Declares slash commands through the client.

print(discord)
bot.remove_command('help')
bot.load_extension('jishaku')

@bot.event
async def on_ready():
    print('Online come', bot.user)
    await bot.change_presence(activity=discord.Streaming(name='r-help per una lista di comandi | rispondo a tutto e tutti', url='https://twitch.tv/starnumber12046'))

guild_ids = [] # Put your server ID in this array.
for a in bot.guilds:
  guild_ids.append(a.id)
@slash.slash(name="ping", description="latenza"")
async def _ping(ctx): # Defines a new "context" (ctx) command called "ping."
    await ctx.respond()
    await ctx.send(f"Pong! ({client.latency*1000}ms)")

for a in os.listdir("./cogs"):
    if a.endswith(".py"):
        if a == 'notload.py':
            pass
        else:
            bot.load_extension(f"cogs.{a[:-3]}")
envfiles.load_dotenv(dotenv_path='.env')
server.keep_alive()
bot.run(os.environ.get('token'))
