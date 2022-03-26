import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        profile = user.public_flags
        badges = ""
        if profile.staff:
            badges += "<:staff:823532641633959936> "

        if profile.verified_bot:
            badges += "<:verify:823532641520189441> "

        if profile.verified_bot_developer:
            badges += "<:verifybotdev:823532349408018452> "

        if profile.partner:
            badges += "<:newpartner:823532641407991809> "

        if profile.bug_hunter:
            badges += "<:catch1:823532349442621490> "

        if profile.bug_hunter_level_2:
            badges += "<:buglv2:823532640531251240> "

        if profile.early_supporter:
            badges += "<:sostegno:823532349592567818> "

        if profile.hypesquad_balance:
            badges += "<:hypesquadbalance:823532641533165638> "

        if profile.hypesquad_bravery:
            badges += "<:hypesquadbraverye:823532641600012309 "

        if profile.hypesquad_brilliance:
            badges += "<:hypesquadbrillance:823532641855733791> "
        try:
            embed = discord.Embed(title=f'{user} info', description=f"""
{badges}
😀: {str(user)}
🆔: {user.id}
📱: {user.is_on_mobile()}""", color=user.color)
            embed.set_thumbnail(url=user.avatar.url)
        except:
            embed = discord.Embed(title=f'{user} info', description=f"""
{badges}
😀: str({user})
🆔: {user.id}
📱: {user.is_on_mobile()}""", color=user.color)
            embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def serverinfo(self, ctx):
        embed=discord.Embed(title=f'{ctx.guild.name} info', description=f"""Nome: {ctx.guild.name}
Numero utenti: {len(ctx.guild.members)}
Numero canali: {len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)}""", color=discord.Color.blurple())
        await ctx.send(embed=embed)
    @commands.command()
    async def say(self, ctx, *, args='Non so che dire... nessuno ha scritto niente! <:DBIlel:623618410315513876>'):
        await ctx.send(args, allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False))

    @commands.command()
    async def triggered(self, ctx):
        pass

    @commands.command()
    async def test(self, ctx):
        def check(m):
            return m.author.id == ctx.author.id and \
                   m.channel.id == ctx.channel.id

        response = await self.bot.wait_for('message', check=check, timeout=10.0 * 60.0)
        await ctx.send(response.content)
        await ctx.send(dir(response))






def setup(bot):
    bot.add_cog(Misc(bot))
