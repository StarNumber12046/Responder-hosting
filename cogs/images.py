import discord
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

def setup(bot):
    bot.add_cog(images(bot))