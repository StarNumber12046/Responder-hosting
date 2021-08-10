import discord, datetime
from discord.ext import commands

class SpotifySync(commands.Cog):
    def __init__(self, bot):
        

        self.bot = bot
    
    @commands.command()
    async def spotify(self, ctx, user:discord.Member=None):
        user = user or ctx.author
        activity = user.activity

        for a in user.activities:
            print(a)

            if isinstance(a, discord.Spotify):
                emb = discord.Embed(title=f"{str(user)} | {a.title} di {a.artist}", description=f"")
                emb.url = "https://open.spotify.com/track/" + a.track_id
                artists = " | ".join(a.artists)
                emb.add_field(name="Artisti", value=artists)
                emb.add_field(name="Album", value=a.album)
                emb.color = a.color

                if a.duration:
                    emb.add_field(name="Durata", value=a.duration, inline=False)
                emb.set_thumbnail(url=a.album_cover_url)
                return await ctx.send(embed=emb)

        print("No user activity")
        return await ctx.send(embed=discord.Embed(title=f"{str(ctx.author)}, abbiamo un problema!", description=f"<@!{user.id}> non sta ascoltando nulla su Spotify!"))






def setup(bot):
    bot.add_cog(SpotifySync(bot))
