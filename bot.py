import discord
from discord.ext import commands


apikey = "RGAPI-5ada3568-d1e4-42c0-a3e2-7b405dc72007"
token = "MTE3MjY2NjI0OTAwNDcxMTk1Ng.GzWHB-.EmzV4yWtRb07vhOCDveHXDAYoCDob7TzXUGIFk"
guild_id = 897225679702229014  # Remplacez YOUR_GUILD_ID par l'ID de votre serveur
channel_id = 908735263465947256  # Remplacez YOUR_CHANNEL_ID par l'ID du canal où envoyer le message

intents = discord.Intents.default()
intents.messages = True  # Active les intentions pour les messages

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    # Récupérer le serveur et le canal où envoyer le message
    guild_id = 897225679702229014
    channel_id = 908735263465947256  
    
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)
    
    # Vérifier si le serveur et le canal existent avant d'envoyer le message
    if guild and channel:
        await channel.send("Je suis maintenant en ligne !")


@bot.command(name="clear")
async def delete(ctx, number: int):
    messages = await ctx.channel.history(limit=number + 1).flatten()

    for each_message in messages:
        await each_message.delete()
 


# Lancer le bot
bot.run(token)


