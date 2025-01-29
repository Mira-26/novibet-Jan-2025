import csv
from collections import defaultdict
import os
import pandas as pd

# compare number of goals in 1st vs 2nd half per league per season


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
leagues_path = os.path.join(base_dir, source_files_folder, football_datasets_folder_name, "leagues.csv") # TODO: add read functionality to utility module
games_path = os.path.join(base_dir, source_files_folder, football_datasets_folder_name, "games.csv") 

shots = load_csv(shots_path)
leagues = load_csv(leagues_path)
games = load_csv(games_path)

# create a dict gameID -> (season,leagueID) from games
# we need these 2 attributes to add to shots
# TODO: add the funcionality to a utility module since it's used in more than one place
game_to_season_league = {}
for game in games:
    game_id = game['gameID']
    game_to_season_league[game_id] = {
        'season': game['season'],
        'leagueID': game['leagueID']
    }

# filter on goals from corners
corner_goal_counts = {}
corner_goals = []
for shot in shots:
         # Filter for goals from corners
        if shot['shotResult'].lower() == "goal" and shot['situation'].lower() == "fromcorner":
            shot['season'] = game_to_season_league[shot['gameID']]['season'] # Add season and leagueID from the mapping
            shot['leagueID'] = game_to_season_league[shot['gameID']]['leagueID']
            #  Determine the half
            half = "First Half" if int(shot['minute']) <= 45 else "Second Half" # TODO: handle bad data

            # Unique key to group goals by season, league and half
            key = (shot['season'], shot['leagueID'], half)
            # initialise if empty
            if key not in corner_goal_counts:
                 corner_goal_counts[key] = 0
            corner_goal_counts[key] += 1

# for each league and each season, find the half with most goals scored
final_result = []
for (season, leagueID, half), count in corner_goal_counts.items():
    for league in leagues:
         if league['leagueID'] == leagueID:
              league_name = league['name']

    final_result.append({
        'football_season': season,
        'league_name': league_name,
        'half': half,
        'corner_goals': count
    })

best_half_per_league_season = {}

# iterate the results and compare corner goals
for result in final_result:
    key = (result['football_season'], result['league_name'])

    # if the key doesn't exist or the current result has more corner goals, update
    if key not in best_half_per_league_season or result['corner_goals'] > best_half_per_league_season[key]['corner_goals']:
        best_half_per_league_season[key] = result

# keep only the required fields
final_results = [
    {
        'football_season': value['football_season'],
        'league_name': value['league_name'],
        'half': value['half']
    }
    for value in best_half_per_league_season.values()
]


output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)
df_results = pd.DataFrame(final_results)
output_file = os.path.join(output_dir, "half_with_most_goals_per_league_and_season.parquet") # TODO: remove hardcoded values
df_results.to_parquet(output_file, engine="pyarrow", index=False)
print(f"Final structured data has been saved to {output_file} in Parquet format within the output folder")

        
