import time
import sqlite3
from tools import get_summoner_id, get_league_entries, get_current_game

API_KEY = "RGAPI-145cab65-6579-49fa-b5b8-84319b4c2dbf"
REGION = "euw1"  # Change this to the appropriate region

# Initialise la connexion à la base de données
conn = sqlite3.connect("joueurs.db")
cursor = conn.cursor()

# Crée la table joueur si elle n'existe pas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS joueur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_du_compte TEXT UNIQUE,
        tier_soloq TEXT,
        division_soloq TEXT,
        lp_soloq INTEGER,
        tier_flex TEXT,
        division_flex TEXT,
        lp_flex INTEGER,
        in_game BOOLEAN
    )
''')
conn.commit()

def addPlayer(nom_du_compte, api_key, region):
    summoner_id = get_summoner_id(nom_du_compte, api_key, region)
    league_entries = get_league_entries(summoner_id, api_key, region)
    
    tier_soloq, division_soloq, lp_soloq = None, None, None
    tier_flex, division_flex, lp_flex = None, None, None
    
    for entry in league_entries:
        if entry['queueType'] == 'RANKED_SOLO_5x5':
            tier_soloq = entry.get('tier', 'UNRANKED')
            division_soloq = entry.get('rank', '')
            lp_soloq = entry.get('leaguePoints', 0)
        elif entry['queueType'] == 'RANKED_FLEX_SR':
            tier_flex = entry.get('tier', 'UNRANKED')
            division_flex = entry.get('rank', '')
            lp_flex = entry.get('leaguePoints', 0)
    
    cursor.execute('''
        INSERT OR REPLACE INTO joueur (
            nom_du_compte, 
            tier_soloq, 
            division_soloq, 
            lp_soloq, 
            tier_flex, 
            division_flex, 
            lp_flex, 
            in_game
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nom_du_compte, tier_soloq, division_soloq, lp_soloq, tier_flex, division_flex, lp_flex, False))
    
    conn.commit()

def insert_or_update_player_data(nom_du_compte, tier_soloq, division_soloq, lp_soloq, tier_flex, division_flex, lp_flex, in_game):
    cursor.execute('''
        INSERT OR REPLACE INTO joueur (
            nom_du_compte, 
            tier_soloq, 
            division_soloq, 
            lp_soloq, 
            tier_flex, 
            division_flex, 
            lp_flex, 
            in_game
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nom_du_compte, tier_soloq, division_soloq, lp_soloq, tier_flex, division_flex, lp_flex, in_game))
    conn.commit()

def get_all_players():
    cursor.execute('SELECT nom_du_compte FROM joueur')
    return [row[0] for row in cursor.fetchall()]

def track():
    while True:
        for summoner_name in get_all_players():
            try:
                summoner_id = get_summoner_id(summoner_name, API_KEY, REGION)
                league_entries = get_league_entries(summoner_id, API_KEY, REGION)
                current_game = get_current_game(summoner_id, API_KEY, REGION)
                
                for entry in league_entries:
                    if entry['queueType'] == 'RANKED_SOLO_5x5':
                        tier_soloq = entry.get('tier', 'UNRANKED')
                        division_soloq = entry.get('rank', '')
                        lp_soloq = entry.get('leaguePoints', 0)
                    elif entry['queueType'] == 'RANKED_FLEX_SR':
                        tier_flex = entry.get('tier', 'UNRANKED')
                        division_flex = entry.get('rank', '')
                        lp_flex = entry.get('leaguePoints', 0)
                    
                cursor.execute('''
                    SELECT tier_soloq, division_soloq, lp_soloq, tier_flex, division_flex, lp_flex, in_game
                    FROM joueur
                    WHERE nom_du_compte = ?
                ''', (summoner_name,))
                
                result = cursor.fetchone()
                old_tier_soloq, old_division_soloq, old_lp_soloq, old_tier_flex, old_division_flex, old_lp_flex, in_game = result
                
                if (
                    old_tier_soloq != tier_soloq or
                    old_division_soloq != division_soloq or
                    old_lp_soloq != lp_soloq or
                    old_tier_flex != tier_flex or
                    old_division_flex != division_flex or
                    old_lp_flex != lp_flex
                ):
                    print(f"{summoner_name} - Updated Stats:")
                    print(f"SoloQ: {tier_soloq} {division_soloq} LP: {lp_soloq}")
                    print(f"Flex: {tier_flex} {division_flex} LP: {lp_flex}")
                    
                    # Vous pouvez ajouter ici une logique pour afficher les changements (win, lose, etc.)
                
                if in_game:
                    print(f"{summoner_name} is in game.")
                
                insert_or_update_player_data(
                    summoner_name,
                    tier_soloq,
                    division_soloq,
                    lp_soloq,
                    tier_flex,
                    division_flex,
                    lp_flex,
                    current_game is not None
                )
                
            except Exception as e:
                print(f"Error retrieving data for {summoner_name}: {str(e)}")
        
        time.sleep(600)  # Wait for 10 minutes before the next update

if __name__ == "__main__":
    new_player_name = "Aykko"
    addPlayer(new_player_name, API_KEY, REGION)
    track()

# Ferme la connexion à la base de données à la fin du script
conn.close()
