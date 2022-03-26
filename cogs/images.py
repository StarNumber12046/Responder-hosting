import discord
import traceback
import random
import aiohttp
from discord.ext import commands


class images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def comment(self, ctx, *, comment):
        all = list(comment.split(' -- '))
        print(all)
        try:
            user = self.bot.get_user(int(all[1]))
        except:
            user = None
        comment = all[0]
        if user is None:
            user = ctx.author
        finded = ' '
        replaced = '%20'
        replaced2 = '%20'
        if int(len(user.display_name)) > 25:
            await ctx.send(f'Non posso completare la richiesta: il nickname è troppo lungo di {int(len(user.display_name) - 25)} caratteri')
        else:
            await ctx.send(f'https://some-random-api.ml/canvas/youtube-comment?avatar={str(user.avatar.url).replace("webp", "png")}&username={user.display_name.replace(finded, replaced)}&comment={comment.replace(finded, replaced2)}')

    @commands.command()
    async def meme(self, ctx):

        "Get a random meme"

        async with ctx.typing():

            emb = discord.Embed()

            try:
                end = False
                sub = random.choice(["memes", "meme", "dankmemes", "me_irl"])
                async with aiohttp.ClientSession() as cs:
                    r_ = await cs.get(f"https://www.reddit.com/r/{sub}/hot.json")
                    meme = await r_.json()

                await cs.close()
                while not end:
                    r = int(random.choice(range(1, 24)))
                    if meme["data"]["children"][r]["data"]["is_self"] == False:
                        url = meme["data"]["children"][r]["data"]["url_overridden_by_dest"]
                        title = meme["data"]["children"][r]["data"]["title"]
                        ups = meme["data"]["children"][r]["data"]["ups"]
                        author = "u/" + \
                            meme["data"]["children"][r]["data"]["author"]
                        subreddit = "r/" + \
                            meme["data"]["children"][r]["data"]["subreddit"]
                        end = True

                    else:
                        end = False

                emb.title = title
                emb.description = f":thumbsup: | {ups}"
                emb.url = url
                emb.set_author(name=author, url=f"https://reddit.com/{author}")
                emb.set_image(url=url)
                emb.set_footer(text=subreddit)

            except Exception as e:
                traceback.print_exc()
                return await ctx.send(e)

        await ctx.send(embed=emb)

    @commands.command()
    async def exp(self, ctx):
        xp = random.randint(100, 900)

        back_xp = random.randint(0, xp)

        next_xp = random.randint(xp, 2000)

        liv = random.randint(1, 10)

        color = str(ctx.author.color).replace('0x', 'x')


        await ctx.send(f"https://vacefron.nl/api/rankcard?username={str(ctx.author.display_name).replace(' ', '%20')}&avatar={str(ctx.author.avatar.url)[:-10].replace('webp', 'png')}&currentxp={xp}&nextlevelxp={next_xp}&previouslevelxp={back_xp}&level={liv}&xpcolor={color[1:]}&isboosting=true&circleavatar=true")

    @commands.command()
    async def rip(self, ctx, user:discord.User = None):
        user = user or ctx.author
        if str(user.avatar_url_as(static_format="png")).endswith("1024"):

            image = str(user.avatar_url_as(static_format="png"))[:-10]
        else:
            image = str(user.avatar_url_as(static_format="png"))
        await ctx.send("https://vacefron.nl/api/grave?user="+image)


def setup(bot):
    bot.add_cog(images(bot))
