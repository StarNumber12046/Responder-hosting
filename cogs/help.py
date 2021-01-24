import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title='Aiuto', description=None, color=discord.Color.blurple())
        embed.add_field(name='Moderazione', value='r-help moderator | Modera il tuo server', inline=False)
        embed.add_field(name='Misc', value='r-help misc | Comandi inutili ma divertenti', inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def moderator(self, ctx):
        embed = discord.Embed(title='Moderazione', description='<> = non obbligatorio | [] = obbligatorio', color=discord.Color.blurple())
        embed.add_field(name='ban', value='r-ban [user] <reason> (Autorizzazione richiesta: bannare membri)', inline=False)
        embed.add_field(name='kick', value='r-kick [user] <reason> (Autorizzazione richiesta: espellere membri)', inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def misc(self, ctx):
        embed = discord.Embed(title='In arrivo...', description=None, color=discord.Color.blurple())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
