import os
import pandas as pd

if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)
    output_dir = os.path.join(current_dir, "output")
    file_path = os.path.join(output_dir, "top_5_scorers_per_league_and_season.parquet")
    # Load the Parquet file into a DataFrame
    df = pd.read_parquet(file_path)

    print(df)
