import discord, aiosqlite
from discord.ext import commands


async def has_profile(self, user: discord.User):
    con = await aiosqlite.connect("./data/economy.db")
    for a in await con.execute("SELECT * from economy"):
        if a[0] == user.id:
            return True

    return False
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def bal(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author

        con = await aiosqlite.connect("./data/economy.db")
        for a in await con.execute("SELECT * from economy"):
            if a[0] == user.id:
                if await has_profile(ctx.author):
                    embed = discord.Embed(title=f"Soldi di {user.display_name}", description=f"{a[1]} coins")
                    break

        await ctx.send(embed=embed)

    @commands.command()
    async def createprofile(self, ctx):
        if not await has_profile(ctx.author):
            con = await aiosqlite.connect("./data/economy.db")
            await con.execute("INSERT into economy (user, balance) VALUES (?, ?)", ctx.author.id, 10)
        else:
            await ctx.send("hai già un profilo!")


def setup(bot):
    bot.add_cog(Economy(bot))
