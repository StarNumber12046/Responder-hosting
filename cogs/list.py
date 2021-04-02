import dbl
import discord
from discord.ext import commands, tasks
import os
import asyncio
import logging
import dotenv
import aiohttp


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.env = dotenv.load_dotenv(".env")
        self.token = os.environ.get("topgg")
        self.dblpy = dbl.DBLClient(self.bot, self.token)



    # The decorator below will work only on discord.py 1.1.0+
    # In case your discord.py version is below that, you can use self.bot.loop.create_task(self.update_stats())

    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        logger.info('Attempting to post server count')
        try:
            await self.dblpy.post_guild_count()
            logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
        except Exception as e:
            logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

    async def has_voted(self, id, user):
        async with aiohttp.ClientSession() as cs:
            data = await cs.get(f"top.gg/api/bots/{id}/check?userId={user}")
            json = await data.json()
            await cs.close()
        if json["voted"] == 1:
            return True
        else:
            return False


def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(TopGG(bot))