import json
import discord
from discord.ext import commands


class errori(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ignore = ('vol', 'tra', 'equalizer', 'appeal_reason', 'amount', 'tempo')

    @commands.command(description='Effettua il check dei permessi del bot')
    @commands.bot_has_permissions(manage_messages=True, attach_files=True, embed_links=True)
    async def setup(self, ctx):
        await ctx.send('Ho tutti i permessi per un corretto funzionamento, ottimo direi!')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            if ctx.guild.id == 714802740345176074 and ctx.channel.id == 714806643535249462:
                await ctx.send('Comando sconosciuto')
        elif isinstance(error, commands.errors.MissingAnyRole):
            if ctx.author.id in self.bot.owner_ids:  # ctx.author.id == self.bot.owner_id: se non è in un team
                await ctx.message.add_reaction('🔥')
                await ctx.reinvoke()
                return
            await ctx.send("Ti manca un ruolo per utilizzare questo comando")
        elif isinstance(error, commands.BotMissingPermissions):
            raw_error = ''
            for x in error.missing_perms:
                raw_error += f'{x} \n'
            ita = raw_error.replace('create_instant_invite', 'Creare inviti').replace('kick_members',
                                                                                      'Espellere Membri').replace(
                'ban_members', 'Bannare Membri').replace('administrator', 'Amministratore').replace('manage_channels',
                                                                                                    'Gestire canali').replace(
                'manage_guild', 'Gestire Server').replace('add_reactions', 'Aggiungere reazioni').replace(
                'view_audit_log', 'Visualizzare il registro attività').replace('priority_speaker',
                                                                               'Priorità di parola').replace('stream',
                                                                                                             'Video').replace(
                'read_messages', 'Leggere Messaggi').replace('view_channel',
                                                             'Leggere i canali testuali e vedere i canali vocali').replace(
                'send_messages', 'Inviare i messaggi').replace('send_tts_messages', 'Usare la sintesi vocale').replace(
                'manage_messages', 'Gestire messaggi').replace('embed_links', 'Incorporare i link').replace(
                'attach_files', 'Allegare i file').replace('read_message_history',
                                                           'Leggere la cronologia dei messaggi').replace(
                'mention_everyone', 'Menziona @everyone, @here  e tutti i ruoli').replace('external_emojis',
                                                                                          'Usare emoji esterni').replace(
                'use_external_emojis', 'Usare emoji esterni').replace('view_guild_insights',
                                                                      'Visualizzare statitiche server').replace(
                'connect', 'Collegarsi alle chat vocale').replace('speak', 'Parlare').replace('mute_members',
                                                                                              'Silenzia membri').replace(
                'deafen_members', "Silenzai l'audio degli altri").replace('move_members', 'Sposta utenti').replace(
                'use_voice_activation', "Usare l'attivazione vocale").replace('change_nickname',
                                                                              'Cambia nickname').replace(
                'manage_nicknames', 'Gestire i soprannomi').replace('manage_roles', 'Gestire i ruoli').replace(
                'manage_permissions', 'Gestire i ruoli').replace('manage_webhooks', 'Gestire i webhook').replace(
                'manage_emojis', 'Gestire gli emoji')
            try:
                embed = discord.Embed(title="", colour=discord.Colour.red())
                embed.add_field(name="⚠ | Mi mancano i seguenti permessi:", value=f'```{ita}```', inline=False)
                await ctx.send(embed=embed)
            except:
                await ctx.send(f'**⚠ | Mi mancano i seguenti permessi:**\n```{ita}```')
        elif isinstance(error, commands.MissingPermissions):
            raw_error = ''
            if ctx.author.id in self.bot.owner_ids:
                await ctx.message.add_reaction('🔥')
                await ctx.reinvoke()
                return
            for x in error.missing_perms:
                raw_error += f'{x} \n'
            ita = raw_error.replace('create_instant_invite', 'Creare inviti').replace('kick_members',
                                                                                      'Espellere Membri').replace(
                'ban_members', 'Bannare Membri').replace('administrator', 'Amministratore').replace('manage_channels',
                                                                                                    'Gestire canali').replace(
                'manage_guild', 'Gestire Server').replace('add_reactions', 'Aggiungere reazioni').replace(
                'view_audit_log', 'Visualizzare il registro attività').replace('priority_speaker',
                                                                               'Priorità di parola').replace('stream',
                                                                                                             'Video').replace(
                'read_messages', 'Leggere Messaggi').replace('view_channel',
                                                             'Leggere i canali testuali e vedere i canali vocali').replace(
                'send_messages', 'Inviare i messaggi').replace('send_tts_messages', 'Usare la sintesi vocale').replace(
                'manage_messages', 'Gestire messaggi').replace('embed_links', 'Incorporare i link').replace(
                'attach_files', 'Allegare i file').replace('read_message_history',
                                                           'Leggere la cronologia dei messaggi').replace(
                'mention_everyone', 'Menziona @everyone, @here  e tutti i ruoli').replace('external_emojis',
                                                                                          'Usare emoji esterni').replace(
                'use_external_emojis', 'Usare emoji esterni').replace('view_guild_insights',
                                                                      'Visualizzare statitiche server').replace(
                'connect', 'Collegarsi alle chat vocale').replace('speak', 'Parlare').replace('mute_members',
                                                                                              'Silenzia membri').replace(
                'deafen_members', "Silenzai l'audio degli altri").replace('move_members', 'Sposta utenti').replace(
                'use_voice_activation', "Usare l'attivazione vocale").replace('change_nickname',
                                                                              'Cambia nickname').replace(
                'manage_nicknames', 'Gestire i soprannomi').replace('manage_roles', 'Gestire i ruoli').replace(
                'manage_permissions', 'Gestire i ruoli').replace('manage_webhooks', 'Gestire i webhook').replace(
                'manage_emojis', 'Gestire gli emoji')
            embed = discord.Embed(title="", colour=discord.Colour.red())
            embed.add_field(name="⚠ | Ti mancano i seguenti permessi:", value=f'```{ita}```', inline=False)
            await ctx.send(embed=embed)
        raise error



def setup(bot):
    bot.add_cog(errori(bot))