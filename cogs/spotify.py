import discord
from discord.ext import commands

class SpotifySync(commands.Cog):
    def __init__(self, bot):
        

        self.bot = bot
    
    @commands.command()
    async def spotify(self, ctx, user:discord.Member=None):
        user = user or ctx.author
        activity = user.activity
        if isinstance(user.activity, discord.Spotify):
            emb = discord.Embed(title=f"{str(user)} | {activity.title} di {activity.artist}", description=f"<@!{user.id}>> sta ascoltando da {str(activity.start)} ({activity.duration})")
            emb.add_field(name="Artista", value=activity.artists)
            emb.add_field(name="Album", value=activity.album)
            emb.color = activity.color
            emb.set_thumbnail(url=activity.album_cover_url)
            await ctx.send(embed=emb)
        else:
            await ctx.send(embed=discord.Embed(title=f"{str(ctx.author)}, abbiamo un problema!", description=f"<@!{user.id}> non sta ascoltando nulla su Spotify!"))



def setup(bot):
    bot.add_cog(SpotifySync(bot))
