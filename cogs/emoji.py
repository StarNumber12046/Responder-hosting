import discord, aiosqlite, random
from discord.ext import commands

class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def emotechannel(self, ctx, channel=discord.TextChannel):
        con = await aiosqlite.connect("./data/misc.db")
        found = False
        async with await con.execute("SELECT * from emojis") as cursor:
            async for row in cursor:
                if row[0] == ctx.guild.id:
                    found = True
                    break
        if found:
            await con.execute(f"UPDATE emojis set channel = {channel.id} WHERE guild = {ctx.guild.id}")
        else:
            await con.execute("INSERT into emojis (guild, channel) VALUES (?, ?)", (ctx.guild.id, channel.id))
        await con.commit()
        await con.close()
        await ctx.send("OK!")

    @emotechannel.command()
    async def remove(self, ctx):
        con = await aiosqlite.connect("./data/misc.db")
        found = False
        async with await con.execute("SELECT * from emojis") as cursor:
            async for row in cursor:
                if row[0] == ctx.guild.id:
                    found = True
                    break

        if found:
            await con.execute(f"DELETE FROM emojis where guild = {ctx.guild.id}")
            await con.commit()

        else:
            await ctx.send("Non hai impostato un canale!!!")
        await con.close()

def setup(bot):
    bot.add_cog(Emoji(bot))