import discord, aiosqlite

from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        con = await aiosqlite.connect("./data/misc.db")
        found = False
        async with con.execute("SELECT * from welcome") as cursor:
            async for row in cursor:
                print(int(row[0]))
                print(int(member.guild.id))
                if int(row[0]) == member.guild.id:
                    g = member.guild
                    print(g)
                    print(member.guild.id)
                    found = True

                    break
            if found is True:
                c = self.bot.get_channel(int(row[1]))
                tosend = row[2].replace(f"<usermention>", f"{member.mention}").replace("<membername>", f"{member.display_name}").replace("<memberdiscrim>", f"{member.discriminator}")
                await c.send(tosend)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        con = await aiosqlite.connect("./data/misc.db")
        found = False
        async with con.execute("SELECT * from leave") as cursor:
            async for row in cursor:
                print(cursor)
                if row[0] == member.guild.id:
                    print(row)
                    g = member.guild
                    found = True
                    break
        print(found)
        if found:
            c = self.bot.get_channel(int(row[1]))
            tosend = row[2].replace(f"<usermention>", f"{member.mention}").replace("<membername>", f"{member.display_name}").replace("<memberdiscrim>", f"{member.discriminator}")
            print(tosend)
            await c.send(tosend)
        await con.close()
    @commands.group(invoke_without_command=True)
    async def join(self, ctx):
        await ctx.send(f"{ctx.prefix}join set #canale messaggio")

    @join.command()
    async def set(self, ctx, channel:discord.TextChannel, *, message = None):
        con = await aiosqlite.connect("./data/misc.db")
        async with con.execute("SELECT * from welcome") as cursor:
            async for row in cursor:
                if channel is None:
                    if int(row[0]) == ctx.guild.id:
                        await ctx.send(f"{self.bot.get_channel(int(row[1])).mention} ({row[2]})\n\n**Variabili**\n<usermention> : menziona l'utente\n<membername> : Nome dell'utente\n<memberdiscrim> : discriminatore (#0000) dell'utente")
                        break
        found = False
        if channel is not None:
            async with con.execute("SELECT * from welcome") as cursor:
                async for row in cursor:
                    if int(row[0]) == ctx.guild.id:
                        found = True

        if found:
            await con.execute(f"Update welcome set channel = ? WHERE guild = ?", (channel.id, ctx.guild.id))
            await con.execute(f"Update welcome set message = ? WHERE guild = ?", (message, ctx.guild.id))
            await con.commit()
            await ctx.send("Messaggio aggiornato")
        else:
            await con.execute("INSERT into welcome (guild, channel, message) VALUES (?, ?, ?)", (ctx.guild.id, channel.id, message))
            await con.commit()
            await ctx.send("Fatto!")
        await con.close()

    @commands.group(invoke_without_command=True)
    async def leave(self, ctx):
        await ctx.send(f"{ctx.prefix}leave set #canale messaggio")

    @leave.command()
    async def set(self, ctx, channel: discord.TextChannel = None, *, message=None):
        con = await aiosqlite.connect("./data/misc.db")
        async with con.execute("SELECT * from leave") as cursor:
            async for row in cursor:
                if channel is None:
                    if int(row[0]) == ctx.guild.id:
                        return await ctx.send(
                            f"{self.bot.get_channel(int(row[1])).mention} ({row[2]})\n\n**Variabili**\n<usermention> : menziona l'utente\n<membername> : Nome dell'utente\n<memberdiscrim> : discriminatore (#0000) dell'utente")
        found = False
        if channel is not None:
            async with con.execute("SELECT * from leave") as cursor:
                async for row in cursor:
                    if int(row[0]) == ctx.guild.id:
                        found = True

        if found:
            await con.execute(f"Update leave set channel = ? WHERE guild = ?", (channel.id, ctx.guild.id))
            await con.execute(f"Update leave set message = ? WHERE guild = ?", (message, ctx.guild.id))
            await con.commit()
            await ctx.send("Messaggio aggiornato")
        else:
            await con.execute("INSERT into leave (guild, channel, message) VALUES (?, ?, ?)",
                              (ctx.guild.id, channel.id, message))
            await con.commit()
            await ctx.send("Fatto!")
        await con.close()


def setup(bot):
    bot.add_cog(Welcome(bot))