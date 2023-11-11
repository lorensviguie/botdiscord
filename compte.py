import requests

api_key = "RGAPI-5ada3568-d1e4-42c0-a3e2-7b405dc72007"
#summoner_name = "Aykko"

def get_summoner_id(summoner_name, api_key):
    url = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        return response.json()['id']
    else:
        print(f"Error {response.status_code}: Unable to retrieve summoner ID.")
        return None

def get_all_league_entries(summoner_id, api_key):
    url = f'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}'
    response = requests.get(url)


    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: Unable to retrieve league entries.")
        return None

def display_all_league_entries(entries):
    result = ""
    for entry in entries:
        summoner_name = entry['summonerName']
        queue_type = entry['queueType']
        tier = entry['tier']
        rank = entry['rank']
        league_points = entry['leaguePoints']
        wins = entry['wins']
        losses = entry['losses']

        winrate = calculate_winrate(wins, losses)

        result += f"**Summoner Name:** {summoner_name}\n"
        result += f"**Queue Type:** {queue_type}\n"
        result += f"**Rank:** {tier} {rank}\n"
        result += f"**League Points:** {league_points}\n"
        result += f"**Wins:** {wins}\n"
        result += f"**Losses:** {losses}\n"
        result += f"**Winrate:** {winrate:.2f}%\n"
        result += "=" * 50 + "\n"
    return result

def calculate_winrate(wins, losses):
    total_games = wins + losses
    if total_games == 0:
        return 0.0
    return wins / total_games * 100


if __name__ == "__main__":
    summoner_id = get_summoner_id(summoner_name, api_key)
    
    if summoner_id:
        all_league_entries = get_all_league_entries(summoner_id, api_key)
        
        if all_league_entries:
            display_all_league_entries(all_league_entries)
