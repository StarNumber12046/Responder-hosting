import discord, aiosqlite, random
from discord.ext import commands


async def has_profile(user: discord.User):
    con = await aiosqlite.connect("./data/economy.db")
    found = False
    async with await con.execute("SELECT * from economy") as cursor:
        async for row in cursor:
            if row[0] == user.id:
                found = True

    await con.close()
    return found

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def bal(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author

        con = await aiosqlite.connect("./data/economy.db")
        async with await con.execute("SELECT * from economy") as cursor:
            if await has_profile(user):
                async for row in cursor:
                    if row[0] == user.id:

                        embed = discord.Embed(title=f"Soldi di {user.display_name}", description=f"{row[1]} coins")
                        await ctx.send(embed=embed)
            else:
                print("No profile")
                embed = discord.Embed(title=f"{user.display_name} Non ha un profilo",
                                      description=f"deve crearlo con {ctx.prefix}createprofile")
                await ctx.send(embed=embed)

        await con.close()
        print(await has_profile(user))



    @commands.command()
    async def createprofile(self, ctx):
        if not await has_profile(ctx.author):
            con = await aiosqlite.connect("./data/economy.db")
            await con.execute("INSERT into economy (user, balance) VALUES (?, ?)", (ctx.author.id, 10))
            await con.commit()
            await con.close()

        else:
            await ctx.send("hai già un profilo!")
    @commands.command()
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def work(self, ctx):
        if not await has_profile(ctx.author):
            await ctx.send("Devi creare un profilo")
            return "not"
        con = await aiosqlite.connect("./data/economy.db")
        rand = random.randint(1, 100)
        async with await con.execute("SELECT * from economy") as cursor:

            print("starting...")
            async for row in cursor:

                print(row)
                print(type(ctx.author.id))
                print("lel")
                print(type(row[0]))
                sus = row[0] == ctx.author.id
                print(sus)
                if sus:
                    bal = int(row[1])
                    print(row[0])
                    print(bal)
        try:
            print(bal)
        except:
            return await ctx.send("OOF")


        await con.execute("UPDATE economy SET balance = ? where user = ?", (bal + rand, ctx.author.id))
        await ctx.send(f"Hai lavorato e hai guadagnato {rand} coins")
        async with await con.execute("SELECT * from economy") as cursor:
            print("starting...")

            async for row in cursor:

                print(row)
                print(type(ctx.author.id))
                print("lel")
                print(type(row[0]))
                sus = row[0] == ctx.author.id
                print(sus)
                if sus:
                    bal = int(row[1])
                    print(row[0])
                    print(bal)
        
        await con.commit()
        await con.close()



def setup(bot):
    bot.add_cog(Economy(bot))
