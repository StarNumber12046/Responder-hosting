import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot)

    @commands.command()
    async def invite(self, ctx, integrer = "1911946966"):
        await ctx.send(embed=discord.Embed(title='Invitami!', description=None, url=f'https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions={integrer}&scope=bot'))

    @commands.command()
    async def support(self, ctx):
        await ctx.send(embed=discord.Embed(title='Server di supporto', description='Chiedi **aiuto**, ottieni le **news** in anticipo e partecipa ai **giveaway**!',
                                           url='https://discord.gg/EzT4zT4'))
    @commands.command()
    async def infos(self, ctx):
        integrer = "1911946966"
        m = await ctx.send("Menu", buttons=[Button(style=ButtonStyle.URL, label="Invito", url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions={integrer}&scope=bot"),
                                            Button(style=ButtonStyle.green, label="Bot"),
                                            Button(style=ButtonStyle.URL, label="Sito ufficiale", url="https://responder.starnumber.tk"),
                                            Button(style=ButtonStyle.URL, label="Vota", url="https://top.gg/bot/725342148488069160/vote")])
        res = await self.bot.wait_for("button_click")
        if not res.channel == ctx.channel:
            return False 
        await res.respond(

            type=InteractionType.ChannelMessageWithSource,
            content=f'Questo bot è stato creato da StarNumber12046. E\'un piccolo bot italiano. Ecco alcune informazioni\nPing: {self.bot.latency * 1000}\nServers: {len(self.bot.guilds)}\nUtenti: {len(self.bot.users)}'
        )

def setup(bot):
    bot.add_cog(Info(bot))
