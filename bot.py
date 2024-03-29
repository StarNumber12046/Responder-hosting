import os

#os.system("pip install -r requirements.txt")

import discord
from discord.ext import commands
import jishaku
import prefix
import dotenv as envfiles
import server
#from discord_slash import SlashCommand, SlashContext
#from discord_slash.utils.manage_commands import create_option

bot = commands.Bot(command_prefix=prefix.get_prefix, intents=discord.Intents.all())
#slash = SlashCommand(bot, sync_commands=True, override_type=True) # Declares slash commands through the client.

print(discord)
bot.remove_command('help')
bot.load_extension('jishaku')

@bot.event
async def on_ready():
    print('Online come', bot.user)
    await bot.change_presence(activity=discord.Streaming(name='r-help per una lista di comandi | rispondo a tutto e tutti', url='https://twitch.tv/starnumber12046'))
"""
@slash.slash(name="ping", description="latenza")
async def _ping(ctx: SlashContext): # Defines a new "context" (ctx) command called "ping."
    try:
        await ctx.respond()
        emb = discord.Embed(title="🏓Pong", description=f"{str(round(bot.latency * 1000))}ms impiegati)", color=discord.Colour.blurple())
        await ctx.send(content="Misurazione eseguita con successo!", embeds=[emb])
    except Exception as e:
        await ctx.respond()
        await ctx.send(content=str(e))

@slash.slash(name="say", description="il bot parla al posto tuo qualcosa", options=[
    create_option(
        name="testo",
        description="Cosa deve dire il bot?",
        option_type=3,
        required=True)])
async def say(ctx:SlashContext, testo : str):
    try:
        await ctx.send(testo)
    except Exception as e:
        error = discord.Embed(title="SI è verificato un problema!", description=e, color=discord.Color.red())
        print(e)
        await ctx.send(embeds=[error])
"""


for a in os.listdir("./cogs"):
    if a.endswith(".py"):
        if a == 'notload.py':
            pass
        else:
            if a in ["spotify.py"]:
                pass
            bot.load_extension(f"cogs.{a[:-3]}")
envfiles.load_dotenv(dotenv_path='.env')
#server.keep_alive()
bot.run(os.environ.get('token'))
