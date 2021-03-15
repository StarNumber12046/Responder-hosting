import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import json
import aiohttp
import os
import io
from urllib.request import urlopen

from datetime import datetime, timedelta
import functools

import subprocess
from typing import Union
import utils
def eng(int : str):
    return(int.replace("1", "one").replace("2", "two").replace("3", "three").replace("4", "four").replace("5", "five").replace("6", "six").replace("7", "seven").replace("8", "eight").replace("9", "nine").replace("0", "zero"))


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases = ["setprefix"], invoke_without_command = True)
    @commands.has_permissions(manage_roles = True)
    async def prefix(self, ctx, *, prefix):

      "Set a custom prefix"

      with open("data/prefixes.json", "r") as f:

        l = json.load(f)

      l[str(ctx.guild.id)] = prefix

      with open("data/prefixes.json", "w") as f:

        json.dump(l, f, indent = 4)

      await ctx.send(f"Il prefisso per **{ctx.guild.name}** è ora `{prefix}`.")

    @prefix.command()
    async def reset(self, ctx):

      "Reset the default prefix"

      with open("data/prefixes.json", "r") as f:

        l = json.load(f)

      try:
        
        l.pop(str(ctx.guild.id))

        with open("data/prefixes.json", "w") as f:

          json.dump(l, f)

        await ctx.send(f"Prefisso resettato a `r-`.")

      except KeyError:

        await ctx.send("Il prefisso è quello di default (`r-`).")
    @commands.command()
    async def poll(self, ctx, *, args):
        options = list(args.split(" | "))
        if len(options) == 1:
            emb = discord.Embed(title=options[0], description=None)
            m = await ctx.send(embed=emb)
            await m.add_reaction(":thumbsup:")
            await m.add_reaction(":thumbsdown:")
        elif len(options) == 2:
            args = list(options.split(" - "))
            if len(args) > 10:
                await ctx.send(f"Hai inserito troppe opzioni (sono {len(args)} ma il massimo è 10)")
            else:
                count = 0
                embed = discord.Embed(title=options[0])
                for i in args:
                    if count < 10:
                        embed.add_field(name=i, value=f":{eng(str(count))}:")
                        count = count + 1

                m = await ctx.send(embed=embed)
                count = 0
                for a in args:
                    if count < 10:
                        await m.add_reaction(f":{eng(str(count))}:")
                        count = count + 1
                    else:
                        break





def setup(bot):
    bot.add_cog(Utility(bot))