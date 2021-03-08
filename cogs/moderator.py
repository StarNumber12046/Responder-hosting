import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason='motivo non precisato'):
        embed = discord.Embed(title='Utente espulso',
                              description=f'Ho espulso l\'utente {user} per il seguente motivo: {reason}', color=discord.Color.blurple())
        await ctx.send(embed=embed)
        await user.kick(reason=reason)




    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)

    async def ban(self, ctx, user: discord.Member, *, reason='motivo non precisato'):
        embed = discord.Embed(title='Utente bannato',
                              description=f'Ho bannato l\'utente {user} per il seguente motivo: {reason}',
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)
        await user.ban(reason=reason)





    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, user: int):
        u = self.bot.get_user(user)
        embed = discord.Embed(title='Utente unbannato',
                              description=f'Ho unbannato l\'utente {u}',
                              color=discord.Color.blurple())

        await ctx.send(embed=embed)
        await ctx.guild.unban(u)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(ctx, member: discord.Member):
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(member)
            perms.send_messages = True
            await channel.set_permissions(member, overwrite=perms, reason=f"UnMuted! (da {ctx.author})")
        await ctx.send(f"{member} è stato smutato.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(ctx, member: discord.Member):
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(member)
            perms.send_messages = False
            await channel.set_permissions(member, overwrite=perms, reason=f"Muted! (da {ctx.author})")
        await ctx.send(f"{member} è stato mutato.")




def setup(bot):
    bot.add_cog(Moderator(bot))
