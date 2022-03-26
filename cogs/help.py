import aiosqlite
import discord, random
from discord.ext import commands
#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


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


class HelpCommand:
    def __init__(self, bot):
        self.bot = bot

    def get_type(self, command):
        "check if a command or a cog is passed"

        if self.bot.get_command(command):
            return "command"

        elif self.bot.get_cog(command):
            return "cog"

        else:
            return None

    async def command_not_found(self, ctx, command):
        "command not found error"
        emb = discord.Embed(description=f"```\ncommand {command} not found!\n```", colour=discord.Colour.red())
        return await ctx.send(embed=emb)

    async def cog_not_found(self, ctx, cog):
        "command not found error"
        emb = discord.Embed(description=f"```\ncog {cog} not found!\n```", colour=discord.Colour.red())
        return await ctx.send(embed=emb)

    async def command_list(self, ctx):
        "return the commands list"

        emb = discord.Embed(title="Help",
                            timestamp=ctx.message.created_at)
        emb.set_author(name=ctx.author, icon_url=str(ctx.author.avatar.url))

        for cog in self.bot.cogs:
            cog_str = ""
            self.bot.clean_prefix = ctx.prefix
            cog = self.bot.get_cog(cog)
            commands = cog.get_commands()
            commands = [cmd for cmd in commands if not cmd.hidden]

            if len(commands) >= 1:
                for command in commands:
                    cog_str += f"{self.bot.clean_prefix}{command.name} {command.signature}\n" if command.signature else f"{self.bot.clean_prefix}{command.name}\n"

                    try:
                        for cmd in command.commands:
                            cog_str += f"{self.bot.clean_prefix}{cmd.parent} {cmd.name}{cmd.signature}\n" if command.signature else f"{self.bot.clean_prefix}{cmd.parent} {cmd.name}\n"
                    except:
                        pass

                emb.add_field(name=cog.qualified_name, value=f"```prolog\n{cog_str}\n```")

        return await ctx.send(embed=emb)

    async def command(self, ctx, command: commands.Command):
        "return single command help"

        if command.hidden:
            return await self.command_not_found(ctx, command.name)

        emb = discord.Embed(title="Help", description=command.help,
                            colour=discord.Colour.from_hsv(random.random(), 1, 1), timestamp=ctx.message.created_at)
        emb.set_author(name=ctx.author, icon_url=str(ctx.author.avatar_url_as(static_format="png")))

        try:
            parent = command.parent
        except:
            parent = None

        if parent:
            usage = f"```{self.bot.clean_prefix}{command.parent} {command.name}{command.signature}```" if command.signature else f"```{self.bot.clean_prefix}{command.parent} {command.name}```"
            emb.add_field(name="Usage", value=usage)

            if command.aliases:
                aliases = "\n".join([f"{self.bot.clean_prefix}{cmd}" for cmd in command.aliases])
                emb.add_field(name="Aliases", value='```\n{}\n```'.format(aliases))

            emb.add_field(name="Parent", value=f"```\n{self.bot.clean_prefix}{command.parent}\n```")

            return await ctx.send(embed=emb)

        else:
            usage = f"```{self.bot.clean_prefix}{command.name} {command.signature}```" if command.signature else f"```{self.bot.clean_prefix}{command.name}```"
            emb.add_field(name="Usage", value=usage)

            if command.aliases:
                aliases = "\n".join([f"{self.bot.clean_prefix}{cmd}" for cmd in command.aliases])
                emb.add_field(name="Aliases", value='```\n{}\n```'.format(aliases))

            try:
                if command.commands:
                    subcommands = ""
                    for cmd in [c for c in command.commands if not c.hidden]:
                        subcommands += f"{self.bot.clean_prefix}{cmd.parent} {cmd.name} {cmd.signature}\n"

                    emb.add_field(name="Subcommands", value=f"```\n{subcommands}\n```")

            except:
                pass

            return await ctx.send(embed=emb)

    async def cog(self, ctx, cog: commands.Cog):
        "return cog commands"

        emb = discord.Embed(title=cog.qualified_name, description="",
                            colour=discord.Colour.from_hsv(random.random(), 1, 1), timestamp=ctx.message.created_at)
        emb.set_author(name=ctx.author, icon_url=str(ctx.author.avatar_url_as(static_format="png")))

        commands = cog.get_commands()
        commands = [cmd for cmd in commands if not cmd.hidden]

        cog_str = ""

        if len(commands) >= 1:
            for command in commands:
                cog_str += f"{self.bot.clean_prefix}{command.name} {command.signature}\n" if command.signature else f"{self.bot.clean_prefix}{command.name}\n"

                try:
                    for cmd in command.commands:
                        cog_str += f"{self.bot.clean_prefix}{cmd.parent} {cmd.name} {cmd.signature}\n" if command.signature else f"{self.bot.clean_prefix}{cmd.parent} {cmd.name}\n"
                except:
                    pass

            emb.description = f"```prolog\n{cog_str}\n```"

        else:
            return await self.cog_not_found(ctx, cog.qualified_name)

        return await ctx.send(embed=emb)
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #DiscordComponents(bot)
        self._original_help_command = bot.help_command
        self.help = HelpCommand(bot)
        bot.help_command = None

    @commands.command(hidden=True)
    async def help(self, ctx, command=None):
        "stop it, get some help"

        if not command:
            await self.help.command_list(ctx)

        else:
            if self.help.get_type(command) == "command":
                await self.help.command(ctx, self.bot.get_command(command))

            elif self.help.get_type(command) == "cog":
                await self.help.cog(ctx, self.bot.get_cog(command))

            else:
                await self.help.command_not_found(ctx, command)


"""
    @commands.command(hidden=True)
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

    @commands.command(hidden=True)
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
"""

def setup(bot):
    bot.add_cog(Help(bot))
