import aiosqlite
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


# async
def is_blacklisted(ctx):
    async def predicate(ctx):
        async with aiosqlite.connect('./data/db.db') as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM blacklist') as cursor:
                async for row in cursor:
                    value = row['user']
                    if int(value) == int(ctx.author.id):
                        return False
                    else:
                        return True

    return commands.check(predicate)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot)

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
        embed = discord.Embed(title='Moderazione', description='<> = non obbligatorio | [] = obbligatorio',
                              color=discord.Color.blurple())
        embed.add_field(name='ban', value=f'{ctx.prefix}ban [user] <reason> (Autorizzazione richiesta: bannare membri)',
                        inline=False)
        embed.add_field(name='kick',
                        value=f'{ctx.prefix}kick [user] <reason> (Autorizzazione richiesta: espellere membri)',
                        inline=False)
        embed.add_field(name='unban', value=f'{ctx.prefix}unban [user] (Autorizzazione richiesta: bannare membri)',
                        inline=False)
        embed.add_field(name="warn",
                        value=f"{ctx.prefix}warn [user] reason (autorizzazione richiesta: gestire messaggi)\navvisa un utente")
        embed.add_field(name="warns", value=f"{ctx.prefix}warns <user>\nvisualizza avvisi di un utente")
        embed.add_field(name="removewarn",
                        value=f"{ctx.prefix}removewarn [id] (autorizzazione richiesta: gestire messaggi)\nrimuove un avviso ad un utente")
        await ctx.send(embed=embed)

    @help.command()
    async def utility(self, ctx):
        embed = discord.Embed(title='Utility', description='<> = non obbligatorio | [] = obbligatorio',
                              color=discord.Color.blurple())
        embed.add_field(name='prefix / setprefix',
                        value=f'{ctx.prefix}setprefix/prefix [nuovo prefisso/reset] \nN.B. reset resetta ad **r-** il prefisso',
                        inline=False)
        embed.add_field(name=f"poll",
                        value=f"{ctx.prefix}poll [titolo sondaggio] | <opzione 1> - <opzione 2> \nN.B. è possibile aggiungere infinite opzioni ma devono essere separate da un **-** . Se non si inseriscono le opzioni sarà inviato un sondaggio con :thumbsup: e :thumbsdown:",
                        inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def info(self, ctx):
        embed = discord.Embed(title='Info sul bot', description='[] = obbligatorio, <> = non obbligatorio',
                              color=discord.Color.blurple())
        embed.add_field(name='Invite',
                        value=f'{ctx.prefix}invite <permissions integrer> (se non si scrive nulla il bot userà i permessi consigliati)',
                        inline=False)
        embed.add_field(name='Support', value=f'{ctx.prefix}support', inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def misc(self, ctx):
        embed = discord.Embed(title='Misc', description='[] = obbligatorio | <> = non obbligatorio',
                              color=discord.Color.blurple())
        embed.add_field(name='userinfo',
                        value=f'{ctx.prefix}userinfo  <utente> (Se non si inserisce un utente il bot restituirà le info dell\'autore del comando)',
                        inline=False)
        embed.add_field(name='serverinfo',
                        value=f'{ctx.prefix}serverinfo',
                        inline=False)
        embed.add_field(name='say', value=f'{ctx.prefix}say [messaggio]', inline=False)
        embed.add_field(name='comment', value=f'{ctx.prefix}comment [commento youtube] -- <id utente>')
        embed.add_field(name="meme", value=f"{ctx.prefix}meme", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def ihelp(self, ctx):
        m = await ctx.send("Help menu", components=[Button(style=ButtonStyle.blue, label="Moderazione"),
                                                 Button(style=ButtonStyle.blue, label="Misc"),
                                                 Button(style=ButtonStyle.blue, label="Info")
                                                 ]
                           )
        res = await self.bot.wait_for("button_click")
        if not res.channel == ctx.channel:
            return False

        if res.component.label == "Moderazione":
            embed = discord.Embed(title='Moderazione', description='<> = non obbligatorio | [] = obbligatorio',
                                  color=discord.Color.blurple())
            embed.add_field(name='ban',
                            value=f'{ctx.prefix}ban [user] <reason> (Autorizzazione richiesta: bannare membri)',
                            inline=False)
            embed.add_field(name='kick',
                            value=f'{ctx.prefix}kick [user] <reason> (Autorizzazione richiesta: espellere membri)',
                            inline=False)
            embed.add_field(name='unban', value=f'{ctx.prefix}unban [user] (Autorizzazione richiesta: bannare membri)',
                            inline=False)
            embed.add_field(name="warn",
                            value=f"{ctx.prefix}warn [user] reason (autorizzazione richiesta: gestire messaggi)\navvisa un utente")
            embed.add_field(name="warns", value=f"{ctx.prefix}warns <user>\nvisualizza avvisi di un utente")
            embed.add_field(name="removewarn",
                            value=f"{ctx.prefix}removewarn [id] (autorizzazione richiesta: gestire messaggi)\nrimuove un avviso ad un utente")
            await m.edit(embed=embed)
            await res.respond(

                type=InteractionType.ChannelMessageWithSource,
                content=f'Menu inviato!'
            )
        elif res.component.label == "Misc":
            embed = discord.Embed(title='Misc', description='[] = obbligatorio | <> = non obbligatorio',
                                  color=discord.Color.blurple())
            embed.add_field(name='userinfo',
                            value=f'{ctx.prefix}userinfo  <utente> (Se non si inserisce un utente il bot restituirà le info dell\'autore del comando)',
                            inline=False)
            embed.add_field(name='serverinfo',
                            value=f'{ctx.prefix}serverinfo',
                            inline=False)
            embed.add_field(name='say', value=f'{ctx.prefix}say [messaggio]', inline=False)
            embed.add_field(name='comment', value=f'{ctx.prefix}comment [commento youtube] -- <id utente>')
            embed.add_field(name="meme", value=f"{ctx.prefix}meme", inline=False)
            await m.edit(embed=embed)
            await res.respond(

                type=InteractionType.ChannelMessageWithSource,
                content=f'Menu inviato'
            )
        elif res.component.label == "Info":
            embed = discord.Embed(title='Info sul bot', description='[] = obbligatorio, <> = non obbligatorio',
                                  color=discord.Color.blurple())
            embed.add_field(name='Invite',
                            value=f'{ctx.prefix}invite <permissions integrer> (se non si scrive nulla il bot userà i permessi consigliati)',
                            inline=False)
            embed.add_field(name='Infos',
                            value=f'{ctx.prefix}infos',
                            inline=False)
            embed.add_field(name='Support', value=f'{ctx.prefix}support', inline=False)
            await m.edit(embed=embed)
            await res.respond(

                type=InteractionType.ChannelMessageWithSource,
                content=f'Menu inviato'
            )
    @commands.command()
    async def testpoll(self, ctx, *, poll):
        await ctx.send(embed=discord.Embed(title="Sondaggio", description=poll), components=[Button(style=ButtonStyle.grey, label="", emoji="👍"), Button(style=ButtonStyle.grey, label="", emoji="👎")])
    @commands.Cog.listener()
    async def on_button_click(self, res):
        print(dir(res))
        if not res.component.emoji and res.component.label:
            return
        await res.channel.send(f"E' stato votato {res.component.emoji}")
        await res.respond(
            type=InteractionType.ChannelMessageWithSource, content=f"Hai votato {res.component.emoji}"
        )


def setup(bot):
    bot.add_cog(Help(bot))
