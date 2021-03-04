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



def setup(bot):
    bot.add_cog(Utility(bot))