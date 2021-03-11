import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title='Aiuto', description=None, color=discord.Color.blurple())
        embed.add_field(name='Moderazione', value=f'{ctx.prefix}help moderator | Modera il tuo server', inline=False)
        embed.add_field(name='Misc', value=f'{ctx.prefix}help misc | Comandi inutili ma divertenti', inline=False)
        embed.add_field(name='Info', value=f'{ctx.prefix}help info | Info sul bot', inline=False)
        embed.add_field(name='Utility', value=f'{ctx.prefix}help utility | Comandi utili', inline=False)
        embed.set_footer(text='C\'è un comando segreto che devi assolutamente trovare! E se lo trovi dillo al mio '
                              'owner StarNumber12046#9008')
        await ctx.send(embed=embed)

    @help.command()
    async def moderator(self, ctx):
        embed = discord.Embed(title='Moderazione', description='<> = non obbligatorio | [] = obbligatorio', color=discord.Color.blurple())
        embed.add_field(name='ban', value=f'{ctx.prefix}ban [user] <reason> (Autorizzazione richiesta: bannare membri)', inline=False)
        embed.add_field(name='kick', value=f'{ctx.prefix}kick [user] <reason> (Autorizzazione richiesta: espellere membri)', inline=False)
        embed.add_field(name='unban', value=f'{ctx.prefix}unban [user] (Autorizzazione richiesta: bannare membri)', inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def utility(self, ctx):
        embed = discord.Embed(title='Utility', description='<> = non obbligatorio | [] = obbligatorio', color=discord.Color.blurple())
        embed.add_field(name='prefix', description=f'{ctx.prefix}setprefix/prefix [nuovo prefisso/reset] N.B. reset resetta ad **r-** il prefisso')
        await ctx.send(embed=embed)

    @help.command()
    async def info(self, ctx):
        embed = discord.Embed(title='Info sul bot', description='[] = obbligatorio, <> = non obbligatorio', color=discord.Color.blurple())
        embed.add_field(name='Invite', value=f'{ctx.prefix}invite | invitami', inline=False)
        embed.add_field(name='Support', value=f'{ctx.prefix}support | server di supporto', inline=False)
        await ctx.send(embed=embed)



    @help.command()
    async def misc(self, ctx):
        embed = discord.Embed(title='Misc', description='[] = obbligatorio | <> = non obbligatorio', color=discord.Color.blurple())
        embed.add_field(name='userinfo', value=f'{ctx.prefix}userinfo  <utente> (Se non si inserisce un utente il bot restituirà le info dell\'autore del comando)',
                        inline=False)
        embed.add_field(name='serverinfo',
                        value=f'{ctx.prefix}serverinfo',
                        inline=False)
        embed.add_field(name='say', value=f'{ctx.prefix}say [messaggio]', inline=False)
        embed.add_field(name='comment', value=f'{ctx.prefix}comment [commento youtube] -- <id utente>')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
