import requests
import json
from datetime import datetime

api_key = "RGAPI-5ada3568-d1e4-42c0-a3e2-7b405dc72007"
summoner_name = 'Aykko'
encrypted_puuid = ''

with open('test.json', 'r') as json_file:
    champion_data = json.load(json_file)

def get_champion_name_by_id(champion_id):
    for champion_name, champion_key in champion_data.items():
        if champion_key == str(champion_id):
            return champion_name
    return "Champion inconnu" 

def get_champion_masteries_by_puuid(encrypted_puuid, api_key):
    url = f'https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{encrypted_puuid}?api_key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur {response.status_code}: Impossible de récupérer les maîtrises des champions.")
        return None

def display_masteries(masteries):
    print("{:<20} {:<25} {:<10} {:<20}".format("Champion", "Points de maîtrise", "Niveau", "Dernière fois joué"))
    print("="*90)
    for mastery in masteries:
        champion_id = mastery['championId']
        champion_name = get_champion_name_by_id(champion_id)
        champion_points = mastery['championPoints']
        champion_level = mastery['championLevel']
        last_play_time = mastery['lastPlayTime']
        
        last_play_time_readable = str(datetime.fromtimestamp(last_play_time / 1000.0))
        
        
        print("{:<20} {:<25} {:<10} {:<20}".format(champion_name, champion_points, champion_level, last_play_time_readable))

def get_summoner_puuid(summoner_name, api_key):
    url = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()['puuid']
    else:
        print(f"Error {response.status_code}: Unable to retrieve PUUID.")
        return None

if __name__ == "__main__":
    summoner_puuid = get_summoner_puuid(summoner_name, api_key)
    
    if summoner_puuid:
        encrypted_puuid = summoner_puuid
        print(f"The PUUID of {summoner_name} is: {summoner_puuid}")

    champion_masteries = get_champion_masteries_by_puuid(encrypted_puuid, api_key)
    
    if champion_masteries:
        display_masteries(champion_masteries)
