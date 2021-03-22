import discord, aiosqlite
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import datetime
class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def removewarn(self, ctx, id:int):
        db = await aiosqlite.connect("./data/mod.db")
        async with db.execute('SELECT * FROM warns') as cursor:
            async for row in cursor:


                if int(row[4]) == id:
                    if str(row[3]) == str(ctx.guild.id):

                        db.execute(f"DELETE FROM warns WHERE id = {id}")
                        await db.commit()
                        await db.close()

        await db.close()


    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason='motivo non precisato'):
        embed = discord.Embed(title='Utente espulso',
                              description=f'Ho espulso l\'utente {user} per il seguente motivo: {reason}', color=discord.Color.blurple())
        await ctx.send(embed=embed)
        await user.kick(reason=reason)
        await user.send(f"sei stato espulso da {ctx.guild.name} per il seguente motivo: {reason}")




    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)

    async def ban(self, ctx, user: discord.Member, *, reason='motivo non precisato'):
        embed = discord.Embed(title='Utente bannato',
                              description=f'Ho bannato l\'utente {user} per il seguente motivo: {reason}',
                              color=discord.Color.blurple())
        await user.ban(reason=reason)
        await ctx.send(embed=embed)
        await user.send(f"sei stato bannato da {ctx.guild.name} per il seguente motivo: {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):

        if reason is None:
            reason = f"warn da parte di {ctx.author}"
        connect = await aiosqlite.connect("./data/mod.db")
        date = datetime.datetime.now().strftime("%d/%m/%Y (%H:%M)")
        re = reason.replace(",", "-").replace("'", "\'").replace('"', '\"')
        allwarns = len(connect.execute('SELECT * FROM warns'))
        await connect.execute("INSERT INTO warns (user, reason, date, guild, id) VALUES (?, ?, ?, ?, ?)", (member.id, re, str(date), str(ctx.guild.id), allwarns))
        await connect.commit()
        await connect.close()
        await ctx.send(f"Ho avvisato l'utente {member.mention} per il seguente motivo: {reason}")

    @commands.command()
    async def warns(self, ctx, user:discord.Member=None):
        if user is None:
            user = ctx.author
        all = ''

        member = user.id
        allwarns = 0

        db = await aiosqlite.connect("./data/mod.db")
        async with db.execute('SELECT * FROM warns') as cursor:
            async for row in cursor:


                allwarns += 1
        await db.close()
        async with db.execute('SELECT * FROM warns') as cursor:
            async for row in cursor:


                if int(row[0]) == member:
                    if str(row[3]) == str(ctx.guild.id):

                        all += f"[ID: {str(row[4])}] {row[1]} ({row[2]})\n"

        await db.close()


        if all == '':
            all = f"Nessuna infrazione trovata per {user.mention}"
        await ctx.send(embed=discord.Embed(title=f"Warns per {user.display_name}#{user.discriminator}", description=all))






    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, user: int):
        u = self.bot.get_user(user)
        embed = discord.Embed(title='Utente unbannato',
                              description=f'Ho unbannato l\'utente {u}',
                              color=discord.Color.blurple())


        await ctx.guild.unban(u)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(member)
            perms.send_messages = True
            await channel.set_permissions(member, overwrite=perms, reason=f"UnMuted! (da {ctx.author})")
        await ctx.send(f"{member} è stato smutato.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(member)
            perms.send_messages = False
            await channel.set_permissions(member, overwrite=perms, reason=f"Muted! (da {ctx.author})")
        await ctx.send(f"{member} è stato mutato.")




def setup(bot):
    bot.add_cog(Moderator(bot))
