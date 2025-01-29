import csv
import os
import pandas as pd
from datetime import datetime


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
teams_path = os.path.join(base_dir, source_files_folder, football_datasets_folder_name, "teams.csv") # TODO: handle hardcoded values with a config file
leagues_path = os.path.join(base_dir, source_files_folder, football_datasets_folder_name, "leagues.csv") # TODO: add read functionality to utility module
games_path = os.path.join(base_dir, source_files_folder, football_datasets_folder_name, "games.csv") 
teamstats_path = os.path.join(base_dir, source_files_folder, football_datasets_folder_name, "teamstats.csv") 


teams  = load_csv(teams_path)
leagues = load_csv(leagues_path)
games = load_csv(games_path)
teamstats = load_csv(teamstats_path)

# Step 1: Filter games from La Liga
for game in games:
    if game['leagueID'] == '4':
       la_liga_games =  game 

la_liga_teams = []
for stat in teamstats:
    for game in la_liga_games:
        if stat['gameID'] in la_liga_games["gameID"]:
            la_liga_teams.append(stat)

monthly_shots = {}
# for each team, calculate every year's month number of shot on target
for stat in la_liga_teams:
    # parse the date
    date = datetime.strptime(stat['date'], '%Y-%m-%d %H:%M:%S')
    # keep the year_month part
    year_month = date.strftime('%Y-%m') 

    if stat['teamID'] not in monthly_shots:
        monthly_shots[stat['teamID']] = {}

    if year_month not in monthly_shots[stat['teamID']]:
        monthly_shots[stat['teamID']][year_month] = 0

    if stat['teamID'] not in monthly_shots:
        monthly_shots[stat['teamID']] = {}
    else:
        monthly_shots[stat['teamID']][year_month] += int(stat['shotsOnTarget'])


#  upon inspecting the results, the values appear suspicious which calls for further investigation.

final_results = monthly_shots

output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)
df_results = pd.DataFrame(final_results)
output_file = os.path.join(output_dir,"monthly_shots_on_target_per_team.parquet")
df_results.to_parquet(output_file, engine="pyarrow", index=False)
print(f"Final structured data has been saved to {output_file} in Parquet format within the output folder")