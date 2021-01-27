import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        ch = self.bot.get_channel(762282815923683359)

        emb = discord.Embed(description=f"""<a:benvenuto:733971340045844510> | {self.bot.user.mention} joined **{guild.name}**!
🆔 | {guild.id}
👤 | {guild.owner}
🔢 | {guild.member_count} Members
🍰 | Created at {guild.created_at.strftime("%m / %d / %Y (%H:%M)")}""", colour=discord.Colour.green())
        emb.set_footer(text=f"{len(self.bot.guilds)} guilds",
                       icon_url=self.bot.user.avatar_url)
        emb.set_thumbnail(url=guild.icon_url)

        if guild.banner:
            emb.set_image(url=guild.banner_url)

        await ch.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        ch = self.bot.get_channel(762282815923683359)

        emb = discord.Embed(description=f"""<a:addio:733971481083772978> | {self.bot.user.mention} left **{guild.name}**!
🆔 | {guild.id}
👤 | {guild.owner}
🔢 | {guild.member_count} Members
🍰 | Created at {guild.created_at.strftime("%m / %d / %Y (%H:%M)")}""", colour=discord.Colour.red())
        emb.set_footer(text=f"{len(self.bot.guilds)} guilds",
                       icon_url=self.bot.user.avatar_url)
        emb.set_thumbnail(url=guild.icon_url)

        if guild.banner:
            emb.set_image(url=guild.banner_url)

        await ch.send(embed=emb)
    



def setup(bot):
    bot.add_cog(Events(bot))
