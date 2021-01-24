import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        if user.nick is None:
            embed = discord.Embed(title=f'{user} info', description=f"""```nickname: {str(user)}
            id: {user.id}
            mobile: {user.is_on_mobile()}```""", color=user.color)
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'{user} info', description=f"""```nickname: {user.nick}
            id: {user.id}
            mobile: {user.is_on_mobile()}````""", color=user.color)
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Misc(bot))
