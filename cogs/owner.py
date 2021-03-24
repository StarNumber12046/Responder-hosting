import inspect
from contextlib import redirect_stdout
from typing import Union

import aiosqlite
import asyncio
import discord
import io
import os
import subprocess
import textwrap
import traceback
from discord.ext import commands

from utils import Git




colour = 0xbf794b


class Owner(commands.Cog, command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.git = Git()
        self.color = discord.Color.blurple()
        self.loop = asyncio.get_event_loop()
        self.sessions = set()

    def get_syntax_error(self, e):
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)



    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command()
    async def emoji(self, ctx, emoji: discord.Emoji = None):

        if emoji.animated:

            await ctx.send(f'`<a:{emoji.name}:{emoji.id}>` - {emoji} - {emoji.id} - {emoji.url}')

        else:

            await ctx.send(f'`<:{emoji.name}:{emoji.id}>` - {emoji} - {emoji.id} - {emoji.url}')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        emb = discord.Embed(title='Caricamento...', colour=self.color)
        emb1 = discord.Embed(title=f'Caricata {extension}!', colour=self.color)
        msg = await ctx.send(embed=emb)
        await asyncio.sleep(0.5)

        try:

            self.bot.load_extension(f'cogs.{extension}')

            await msg.edit(embed=emb1)

        except Exception as e:

            traceback.print_exc()

            error = discord.Embed(title=f"""UH! There was an error with {extension}!""", description=str(e),
                                  colour=self.color)
            await msg.edit(embed=error)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, extension=None):
        """reload a cog"""

        async with ctx.typing():
            await self.git.pull(self.bot.loop)

            if not extension:
                emb = discord.Embed(description=f"<:streaming:736511988594638878> | Ricaricamento in corso...",
                                    colour=self.color)
                msg = await ctx.send(embed=emb)
                emb.description = ""

                for cog in os.listdir("./cogs"):
                    if cog.endswith(".py"):
                        try:
                            self.bot.unload_extension(f"cogs.{cog[:-3]}")
                            self.bot.load_extension(f"cogs.{cog[:-3]}")
                        except:
                            emb.description += f"<:dboatsDnd:736511781874303006> {cog[:-3]}\n"
                        else:
                            emb.description += f"<:unmute:736511664614277200> {cog[:-3]}\n"

                return await msg.edit(content=None, embed=emb)

            emb = discord.Embed(description=f"<:streaming:736511988594638878> | Ricarico {extension}",
                                colour=self.color)
            msg = await ctx.send(embed=emb)

            try:
                self.bot.unload_extension(f"cogs.{extension}")
                self.bot.load_extension(f"cogs.{extension}")
            except Exception as e:
                emb.description = f"<:dboatsDnd:736511781874303006> | {extension}\n```bash\n{e}\n```"
            else:
                emb.description = f"<:unmute:736511664614277200> {extension}"

            await msg.edit(content=None, embed=emb)
    @commands.command(pass_context=True, hidden=True)
    async def repl(self, ctx):
        """Launches an interactive REPL session."""
        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': ctx.message,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            '_': None,
        }

        if ctx.channel.id in self.sessions:
            await ctx.send('Already running a REPL session in this channel. Exit it with `quit`.')
            return

        self.sessions.add(ctx.channel.id)
        await ctx.send('Enter code to execute or evaluate. `exit()` or `quit` to exit.')

        def check(m):
            return m.author.id == ctx.author.id and \
                   m.channel.id == ctx.channel.id and \
                   m.content.startswith('`')

        while True:
            try:
                response = await self.bot.wait_for('message', check=check, timeout=10.0 * 60.0)
            except asyncio.TimeoutError:
                await ctx.send('Exiting REPL session.')
                self.sessions.remove(ctx.channel.id)
                break

            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await ctx.send('Exiting.')
                self.sessions.remove(ctx.channel.id)
                return

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await ctx.send(self.get_syntax_error(e))
                    continue

            variables['message'] = response

            fmt = None
            stdout = io.StringIO()

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = f'```py\n{value}{traceback.format_exc()}\n```'
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = f'```py\n{value}{result}\n```'
                    variables['_'] = result
                elif value:
                    fmt = f'```py\n{value}\n```'

            try:
                if fmt is not None:
                    if len(fmt) > 2000:
                        await ctx.send('Content too big to be printed.')
                    else:
                        await ctx.send(fmt)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await ctx.send(f'Unexpected error: `{e}`')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        emb = discord.Embed(title='Caricamento...', colour=self.color)
        emb1 = discord.Embed(title=f'Scaricata {extension}!', colour=self.color)
        msg = await ctx.send(embed=emb)
        await asyncio.sleep(0.5)

        try:

            self.bot.unload_extension(f'cogs.{extension}')

            await msg.edit(embed=emb1)

        except Exception as e:

            traceback.print_exc()

            error = discord.Embed(title=f"""UH! Si è verificato un errore in {extension}!""", description=str(e),
                                  colour=self.color)
            await msg.edit(embed=error)

    @commands.command()
    @commands.is_owner()
    async def asyncio(self, ctx, time, times=None, *, thing=None):

        "Sleep little Satoru"

        if not times:
            times = 1

        if thing:

            thing = f"**{thing}**"

        else:

            thing = " "

        await ctx.message.add_reaction("\U0001f44d")

        for a in range(int(times)):
            await asyncio.sleep(int(time))

        before = ctx.message.created_at

        await ctx.send(f"{ctx.author.mention}, at `{before.strftime('%d %b %Y - %I:%M %p')}` {thing}")

    @commands.command()
    @commands.is_owner()
    async def nick(self, ctx, *, nick):

        "Nickname the bot"

        await ctx.guild.me.edit(nick=nick)
        await ctx.message.add_reaction("<:unmute:736511664614277200>")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
            'owner': self.bot.get_user(488398758812319745)
        }

        env.update(globals())

        body = self.cleanup_code(body)

        body = f"import asyncio\nimport aiosqlite\nimport os\nimport aiohttp\nimport random\nimport humanize\n{body}"

        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.message.add_reaction("<:dboatsDnd:736511781874303006>")
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('<:unmute:736511664614277200>')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(value)
            else:
                self._last_result = ret
                await ctx.send(f'{value}{ret}')

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        "restart the bot"

        await ctx.message.add_reaction("👋")
        subprocess.call("python3 main.py", shell=True)
        await self.bot.close()

    @commands.group(invoke_without_command=True, aliases=["sql"])
    @commands.is_owner()
    async def sqlite(self, ctx, *, command):
        "run a sqlite command"

        command = eval(f"f'{command}'")

        async with aiosqlite.connect("data/db.db") as db:
            data = await db.execute(command)

            if command.lower().startswith("select"):
                data = await data.fetchall()
                emb = discord.Embed(description=f"```py\n{data}\n```", colour=self.color)
                await ctx.send(embed=emb)

            await db.commit()

        await ctx.message.add_reaction("<:unmute:736511664614277200>")

    @commands.command(aliases=["bl"])
    @commands.is_owner()
    async def blacklist(self, ctx, member: Union[discord.Member, discord.User] = None):
        "blacklist a user"

        async with ctx.typing():
            async with aiosqlite.connect("data/db.db") as db:
                if member:
                    await db.execute(f"INSERT into blacklist (user) VALUES ({member.id})")
                    await db.commit()

                else:
                    data = await db.execute(f"SELECT * from blacklist")
                    data = await data.fetchall()

                    emb = discord.Embed(description=f"These users are blacklisted:\n", colour=self.color)

                    for user in data:

                        if int(user[0]) == 0:
                            pass

                        else:
                            u = self.bot.get_user(int(user[0]))
                            if not u:
                                emb.description += f"• **{user[0]}** (I cannot see this user)\n"

                            else:
                                emb.description += f"• **{u}**\n"

                    return await ctx.send(embed=emb)

            emb = discord.Embed(description=f"<:unmute:736511664614277200> | Blacklisted **{member}**",
                                colour=self.color)
            await ctx.send(embed=emb)
            await ctx.message.add_reaction("<:unmute:736511664614277200>")

    @commands.command(aliases=["ubl"])
    @commands.is_owner()
    async def unblacklist(self, ctx, member: Union[discord.Member, discord.User] = None):
        "blacklist a user"

        async with ctx.typing():
            async with aiosqlite.connect("data/db.db") as db:
                await db.execute(f"UPDATE blacklist set user = 0 where user = {member.id}")
                await db.commit()

            emb = discord.Embed(description=f"<:unmute:736511664614277200> | Unblacklisted **{member}**",
                                colour=self.color)
            await ctx.send(embed=emb)
            await ctx.message.add_reaction("<:unmute:736511664614277200>")


def setup(bot):
    bot.add_cog(Owner(bot))
