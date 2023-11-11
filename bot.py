import discord
from discord.ext import commands
import json
from compte import get_all_league_entries , get_summoner_id ,display_all_league_entries ,api_key
from mastery import get_champion_masteries_by_puuid , get_champion_name_by_id ,get_summoner_puuid , format_masteries

apikey = "" #youre api key
token = "" #your token bot
guild_id = 897225679702229014  # Remplacez YOUR_GUILD_ID par l'ID de votre serveur
channel_id = 908735263465947256  # Remplacez YOUR_CHANNEL_ID par l'ID du canal où envoyer le message

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix = "!", intents = intents )

@bot.event
async def on_ready():
    print("le bot est pret")
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    if guild and channel:
        await channel.send("Je suis maintenant en ligne !")

@bot.command(name="lol")
async def get_league_info(ctx, queue_type='', *, summoner_name):
    summoner_id = get_summoner_id(summoner_name, api_key)
    if summoner_id:
        all_league_entries = get_all_league_entries(summoner_id, api_key)

        if all_league_entries:
            if queue_type.lower() == 's':
                soloq_entries = [entry for entry in all_league_entries if entry['queueType'] == 'RANKED_SOLO_5x5']
                league_info = display_all_league_entries(soloq_entries)
            elif queue_type.lower() == 'f':
                flex_entries = [entry for entry in all_league_entries if entry['queueType'] == 'RANKED_FLEX_SR']
                league_info = display_all_league_entries(flex_entries)
            else:
                league_info = display_all_league_entries(all_league_entries)

            await ctx.send(f"Informations sur les ligues de {summoner_name} ({queue_type.upper()}):\n{league_info}")
        else:
            await ctx.send("Impossible de récupérer les informations sur les ligues.")
    else:
        await ctx.send("Impossible de récupérer l'ID du summoner.")

@get_league_info.error
async def lol_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Argument manquant. Essayez \n `!lol S <summoner_name>`\n ou `!lol F <summoner_name>`\n ou `!lol ALL <summoner_name>`.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Argument manquant. Essayez \n `!lol S <summoner_name>`\n ou `!lol F <summoner_name>`\n ou `!lol ALL <summoner_name>`.")

@bot.command(name="mastery")
async def display_mastery(ctx, summoner_name):
    summoner_puuid = get_summoner_puuid(summoner_name, api_key)

    if summoner_puuid:
        encrypted_puuid = summoner_puuid
        await ctx.send(f"The Champion Mastery list of {summoner_name}")

    champion_masteries = get_champion_masteries_by_puuid(encrypted_puuid, api_key)

    if champion_masteries:
        formatted_masteries = format_masteries(champion_masteries)
        
        for chunk in [formatted_masteries[i:i + 2000] for i in range(0, min(len(formatted_masteries), 60000), 2000)]:
            await ctx.send(chunk)

bot.run(token)

