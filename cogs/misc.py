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
            embed = discord.Embed(title=f'{user} info', description=f"""```md
<nickname>: {str(user)}
<id>: {user.id}
<mobile>: {user.is_on_mobile()}```""", color=user.color)
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'{user} info', description=f"""```md
<nickname>: {user.nick}
<id>: {user.id}
<mobile>: {user.is_on_mobile()}```""", color=user.color)
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
    @commands.command()
    async def serverinfo(self, ctx):
        embed=discord.Embed(title=f'{ctx.guild.name} info', description=f"""Nome: {ctx.guild.name}
Numero utenti: {len(ctx.guild.members)}
Numero canali: {len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)}""", color=discord.Color.blurple())




def setup(bot):
    bot.add_cog(Misc(bot))
