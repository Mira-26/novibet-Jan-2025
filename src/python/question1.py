
import csv
from collections import defaultdict
import os
import pandas as pd

# the top 5 top scorers per league per season
# secondary criteria total shots


# Load datasets
def load_csv(filepath): #TODO: move read funcionallity in separate support file
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# Construct the file path dynamically
source_files_folder = "source_files"
football_datasets_folder_name = "football_datasets"
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
shots_path = os.path.join(base_dir, source_files_folder, football_datasets_folder_name, "shots.csv") # TODO: handle hardcoded values with a config file
players_path = os.path.join(base_dir, source_files_folder, football_datasets_folder_name, "players.csv") # TODO: add read functionality to utility module
leagues_path = os.path.join(base_dir, source_files_folder, football_datasets_folder_name, "leagues.csv")
games_path = os.path.join(base_dir, source_files_folder, football_datasets_folder_name, "games.csv") 

shots = load_csv(shots_path)
players = load_csv(players_path)
leagues = load_csv(leagues_path)
games = load_csv(games_path)


# create a dict gameID -> (season,leagueID) from games
# we need these 2 attributes to add to shots
# TODO: add the funcionality to a utility module since it's used in more than one place
game_to_season_league = {}
for game in games:
    game_to_season_league[game['gameID']] = {
        'season': game['season'],
        'leagueID': game['leagueID']
    }

player_goals = {}
for shot in shots:

    if shot['gameID'] in game_to_season_league: #  check data is not missing
        shot['season'] = game_to_season_league[shot['gameID']]['season'] # append season col in shots
        shot['leagueID'] = game_to_season_league[shot['gameID']]['leagueID'] # append leagueID col in shots

    primary_key = (shot['season'], shot['leagueID'], shot['shooterID']) # get all goals/shots by (player,season,league)


    if primary_key not in player_goals:
        player_goals[primary_key] = {'total_goals': 0, 'total_shots': 0} # initialise on first try

    player_goals[primary_key]['total_shots'] += 1 # add the shot

    if shot['shotResult'].lower() == "goal": # if exists, add the goal
        player_goals[primary_key]['total_goals'] += 1

# map out to metadata such as player name and league name
full_results = []
for (season, leagueID, shooterID), _ in player_goals.items():
    for player in players:
         if player['playerID'] == shooterID:
             player_name = player['name']
    
    for league in leagues:
        if league['leagueID'] == leagueID:
            league_name = league['name']

    full_results.append({
        'football_season': season,
        'league_name': league_name,
        'player_name': player_name,
        'total_goals': _['total_goals'],
        'total_shots': _['total_shots']
    })

# sort
full_results.sort(key=lambda x: (x['football_season'], x['league_name'], -x['total_goals'], -x['total_shots']))

final_results = []
checked = {}  # To track the count of players per league and season
for result in full_results:
    key = (result['football_season'], result['league_name'])
    if key not in checked:
        checked[key] = 0
    if checked[key] < 5:  # Limit to top 5 players
        final_results.append(result)
        checked[key] += 1

print("Top 5 Players with Most Goals Per League and Season:")
for result in final_results:
    print(f"Season: {result['football_season']}, League: {result['league_name']}, Player: {result['player_name']}, Goals: {result['total_goals']}, Shots: {result['total_shots']}")
    
output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)
# convert to pandas and store as parquet file
df_results = pd.DataFrame(final_results)
output_file = os.path.join(output_dir, "top_5_scorers_per_league_and_season.parquet") # TODO: remove hardcoded values
df_results.to_parquet(output_file, engine="pyarrow", index=False)
print(f"Final structured data has been saved to {output_file} in Parquet format within the output folder")
