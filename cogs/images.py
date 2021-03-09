import discord, traceback, random, aiohttp
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
            await ctx.send(f'https://some-random-api.ml/canvas/youtube-comment?avatar={str(user.avatar_url).replace("webp", "png")}&username={user.display_name.replace(finded, replaced)}&comment={comment.replace(finded, replaced2)}')
    @commands.command()
    async def meme(self, ctx):
      
      "Get a random meme"

      async with ctx.typing():
        
        emb = discord.Embed(colour = 0x2F3136)

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
              author = "u/" + meme["data"]["children"][r]["data"]["author"]
              subreddit = "r/" + meme["data"]["children"][r]["data"]["subreddit"]
              end = True 

            else:
              end = False

          emb.title = title
          emb.description = f"<a:upvote:639355848031993867> | {ups}"
          emb.url = url
          emb.set_author(name = author, url = f"https://reddit.com/{author}")
          emb.set_image(url = url)
          emb.set_footer(text = subreddit)

        except Exception as e:
          traceback.print_exc()
          return await ctx.send(e)

      await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(images(bot))