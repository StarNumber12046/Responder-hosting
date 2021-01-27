from discord.ext import commands
import discord
import asyncio
import aiohttp
from contextlib import redirect_stdout
import traceback
import textwrap
import io
import os
import json
import inspect


prefix = 'm!!'


def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    # remove `foo`
    return content.strip('` \n')


async def mystbin(data):
    data = bytes(str(data), 'utf-8')
    async with aiohttp.ClientSession() as cs:
        async with cs.post('https://mystb.in/documents', data=data) as r:
            res = await r.json()
            return f'https://mystb.in/{res["key"]}.python'


class owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(aliases=['eval_'], description='SUDO', pass_context=True, hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, body: str = None):
        if body:
            if ctx.author.id == 647092382503796740:
                env = {

                    'bot': self.bot,
                    'self': self,
                    'ctx': ctx,
                    'channel': ctx.channel,
                    'author': ctx.author,
                    'guild': ctx.guild,
                    'message': ctx.message,
                    '_': self._last_result
                }

                env.update(globals())

                body = cleanup_code(body)
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
                    await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
                else:
                    value = stdout.getvalue()
                    try:
                        await ctx.message.add_reaction('\u2705')
                    except:
                        pass

                    if ret is None:
                        if value:
                            await ctx.send(f'```py\n{value}\n```')
                    else:
                        self._last_result = ret
                        await ctx.send(f'```py\n{value}{ret}\n```')
        else:
            await ctx.send('What do I test?')

    @commands.command(description='Load extension', hidden=True)
    @commands.is_owner()
    async def load(self, ctx,  *, extension):
        for extension in extension.split(' '):
            try:
                self.bot.load_extension(f'cogs.{extension}')

                await ctx.message.add_reaction("✅")
            except Exception as e:
                await ctx.message.add_reaction("❌")
                await ctx.send(str(e))

    @commands.command(description='Unload extension', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, extension):
        for extension in extension.split(' '):
            try:
                self.bot.unload_extension(f'cogs.{extension}')

                await ctx.message.add_reaction("✅")
            except Exception as e:
                await ctx.message.add_reaction("❌")
                await self.bot.get_channel(714813858530721862).send(str(e))

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        try:

            os.system('git pull https://starnumber12046:sCVt8PSP3^1UD3wG@github.com/starnumber12046/Responder-hosting.git')
            await ctx.send('Done!')

        except Exception as e:
            await ctx.send('Error!\n' + e)

    @commands.command(description='Reload extension', hidden=True)
    @commands.is_owner()
    async def cogreload(self, ctx, *, extension):
        for extension in extension.split(' '):
            try:
                os.system(
                    'git pull https://starnumber12046:sCVt8PSP3^1UD3wG@github.com/starnumber12046/Responder-hosting.git')
                self.bot.unload_extension(f'cogs.{extension}')
                self.bot.load_extension(f'cogs.{extension}')

                await ctx.message.add_reaction("✅")
            except Exception as e:
                await ctx.message.add_reaction("❌")
                await ctx.send(e)

    @commands.command(description='Show cogs', hidden=True)
    @commands.is_owner()
    @commands.bot_has_permissions(embed_links=True)
    async def cogs(self, ctx):
        cogsloaded = ''
        cogsunloaded = ''
        embed = discord.Embed(title="Index", colour=discord.Colour(
            0xFCFCFC), timestamp=ctx.message.created_at)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        for x in self.bot.cogs:
            cogsloaded += f'{x}\n'

        embed.add_field(name=f"Loaded Cogs:",
                        value=f'```\n{cogsloaded}```', inline=False)

        for x in os.listdir('./cogs'):
            if x.endswith('.py'):
                if x[:-3] not in cogsloaded:
                    cogsunloaded += f'{x[:-3]}\n'

        embed.add_field(name=f"Unloaded Cogs:",
                        value=f'```\n{cogsunloaded}```', inline=False)
        await ctx.send(embed=embed)

    @commands.command(description='Show owner commands', hidden=True)
    @commands.is_owner()
    @commands.bot_has_permissions(embed_links=True)
    async def owner(self, ctx):
        embed = discord.Embed(title="Owner Panel", colour=discord.Colour.blurple(
        ), timestamp=ctx.message.created_at)

        embed.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar_url}")

        for x in self.bot.commands:
            if x.hidden:
                if not x.description:
                    embed.add_field(name=f"{x.name}", value=f'404',
                                    inline=False)
                else:
                    embed.add_field(name=f"{x.name}",
                                    value=f'```{x.description}```', inline=False)

        msg = await ctx.send(embed=embed)
        await msg.delete(delay=60)

    @commands.command(description='Stop bot', hidden=True)
    @commands.is_owner()
    async def stop(self, ctx):
        await ctx.send("Turning off...")
        await self.bot.logout()

    @commands.command(description='Restart the bot', hidden=True)
    @commands.is_owner()
    async def restart(self, ctx):
        try:

            await ctx.send("Restarting...")
            os.system(
                'git pull https://starnumber12046:sCVt8PSP3^1UD3wG@github.com/starnumber12046/matbot.git')

            await self.bot.logout()
            os.system('pip3 install -r requirements.txt')
            os.system("python3 bot.py")

        except:
            await ctx.send('Error!')

    @commands.command(aliases=['up'], description='Load a file', hidden=True)
    @commands.is_owner()
    async def upload(self, ctx, *, arg=None):
        if arg:
            if '/' in arg:
                if ctx.message.attachments:
                    filename = ctx.message.attachments[0].filename
                    attachment = ctx.message.attachments[0].url
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment) as resp:
                            file = await resp.read()
                            try:
                                with open(arg + filename, 'wb') as f:
                                    f.write(file)
                                    f.close()
                            except FileNotFoundError:
                                return await ctx.send('Nope')
                    await ctx.send(f'✅: {arg + filename}')
            else:
                await ctx.send('folder`/`')
        else:
            if ctx.message.attachments:
                filename = ctx.message.attachments[0].filename
                attachment = ctx.message.attachments[0].url
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment) as resp:
                        file = await resp.read()
                        try:
                            with open('cogs/' + filename, 'wb') as f:
                                f.write(file)
                                f.close()
                        except FileNotFoundError:
                            return await ctx.send('Nope')
                await ctx.send(f'✅: cogs/{filename}')

    @commands.command(description="create an invite", hidden=True)
    @commands.is_owner()
    async def get(self, ctx, ID=None):
        if ID:
            try:
                ID = int(ID)
            except:
                return await ctx.send("Id must be a numner")
            g = discord.utils.get(self.bot.guilds, id=ID)
            if any(l.id == ID for l in self.bot.guilds):
                try:
                    for a in g.text_channels:
                        return await ctx.send(await a.create_invite(max_uses=1))
                except:
                    pass
            else:
                await ctx.send('I\'m not in the server')
        else:
            return await ctx.send("Give me ID")

    @commands.is_owner()
    @commands.command(description='send source-link', hidden=True)
    async def source(self, ctx, *, command):
        cmd = self.bot.get_command(command)
        if not cmd:
            emb = discord.Embed(description=f"<:PepeKMS:719317573493194883> | Commando **{command}** non trovato.",
                                colour=discord.Colour.red())
            return await ctx.send(embed=emb)

        try:
            source_lines, _ = inspect.getsourcelines(cmd.callback)
        except (TypeError, OSError):
            emb = discord.Embed(description=f"<:PepeKMS:719317573493194883> | I can't get the source of the command **{command}**.",
                                colour=discord.Colour.red())
            return await ctx.send(embed=emb)

        source_lines_ = ''.join(source_lines)

        await ctx.send(await mystbin(source_lines_))


def setup(bot):
    bot.add_cog(owner(bot))
