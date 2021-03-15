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
    return(int.replace("1", "\U0001f1e6").replace("2", "\U0001f1e7").replace("3", "\U0001f1e8").replace("4", "\U0001f1e9").replace("5", "\U0001f1ea").replace("6", "\U0001f1eb").replace("7", "\U0001f1ec").replace("8", "\U0001f1ed").replace("9", "\U0001f1ee:").replace("0", "\U0001f1ef"))


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
            await m.add_reaction("\U0001f44e")
            await m.add_reaction("\U0001f44d")
        elif len(options) == 2:
            args = list(options[1].split(" - "))
            if len(args) > 10:
                await ctx.send(f"Hai inserito troppe opzioni (sono {len(args)} ma il massimo è 10)")
            else:
                count = 0
                embed = discord.Embed(title=options[0])
                for i in args:
                    if count < 10:
                        embed.add_field(name=i, value=f"{eng(str(count))}", inline=False)
                        count = count + 1

                m = await ctx.send(embed=embed)
                count = 0
                for a in args:
                    if count < 10:
                        await m.add_reaction(f"{eng(str(count))}")
                        count = count + 1
                    else:
                        break





def setup(bot):
    bot.add_cog(Utility(bot))