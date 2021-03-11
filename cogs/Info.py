import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(embed=discord.Embed(title='Invitami!', description=None, url='https://discord.com/api/oauth2/authorize?client_id=725342148488069160&permissions=1911946966&scope=bot'))

    @commands.command()
    async def support(self, ctx):
        await ctx.send(embed=discord.Embed(title='Server di supporto', description='Chiedi aiuto e partecipa ai giveaway',
                                           url='https://discord.gg/EzT4zT4'))
def setup(bot):
    bot.add_cog(Info(bot))
