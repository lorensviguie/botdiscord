import requests

api_key = "RGAPI-5ada3568-d1e4-42c0-a3e2-7b405dc72007"
summoner_name = "Aykko"

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
    print("{:<20} {:<15} {:<10} {:<10} {:<10} {:<10} {:<10} {:<15}".format(
        "Summoner Name", "Queue Type", "Tier", "Rank", "League Points", "Wins", "Losses", "Promo Status"
    ))
    print("=" * 90)
    for entry in entries:
        summoner_name = entry['summonerName']
        queue_type = entry['queueType']
        tier = entry['tier']
        rank = entry['rank']
        league_points = entry['leaguePoints']
        wins = entry['wins']
        losses = entry['losses']

        promo_status = ""
        if 'miniSeries' in entry:
            mini_series = entry['miniSeries']
            promo_status = f"{mini_series['wins']}W-{mini_series['losses']}L"

        print("{:<20} {:<15} {:<10} {:<10} {:<10} {:<10} {:<10} {:<15}".format(
            summoner_name, queue_type, tier, rank, league_points, wins, losses, promo_status
        ))

if __name__ == "__main__":
    summoner_id = get_summoner_id(summoner_name, api_key)
    
    if summoner_id:
        all_league_entries = get_all_league_entries(summoner_id, api_key)
        
        if all_league_entries:
            display_all_league_entries(all_league_entries)
