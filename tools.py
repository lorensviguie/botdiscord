import requests

def get_summoner_id(summoner_name, api_key, region):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    return response.json()["id"]

def get_league_entries(summoner_id, api_key, region):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    return response.json()

def get_current_game(summoner_id, api_key, region):
    url = f"https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None
