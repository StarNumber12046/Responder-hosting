import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx, integrer = "1911946966"):
        await ctx.send(embed=discord.Embed(title='Invitami!', description=None, url=f'https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions={integrer}&scope=bot'))

    @commands.command()
    async def support(self, ctx):
        await ctx.send(embed=discord.Embed(title='Server di supporto', description='Chiedi **aiuto**, ottieni le **news** in anticipo e partecipa ai **giveaway**!',
                                           url='https://discord.gg/EzT4zT4'))
def setup(bot):
    bot.add_cog(Info(bot))
