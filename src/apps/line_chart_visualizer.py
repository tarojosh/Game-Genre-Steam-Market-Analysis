import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re
import datetime

from collections import defaultdict

csv_folder_path = 'src/data/formatted_csv_files' 


def main():
    data = load_snapshots(csv_folder_path)
    
    # # Now we load the data into a line chart 
    chart_timeline(data)


def chart_timeline(data):
    # Line chart
    # X = dates of the snapshot
    # Y = A game's placement on the top selling page
    game_placements = defaultdict(list)
    dates = sorted(data.keys())
    
    for date in dates:
        df = data[date]
        for _, row in df.iterrows():
            game_name = row['name']
            placement = row['placement']
            game_placements[game_name].append((date, placement))
    
    plt.figure(figsize=(12, 6))
    for game_name, timeline in game_placements.items():
        timeline.sort()  # sort by date
        game_dates = [t[0] for t in timeline]
        placements = [t[1] for t in timeline]
        plt.plot(game_dates, placements, label=game_name, marker='o')
    
    plt.gca().invert_yaxis()
    plt.xlabel("Date")
    plt.ylabel("Top Seller Placement")
    plt.title("Top Seller Placement Over Time")
    plt.xticks(rotation=45)
    plt.legend(fontsize='small', loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()
    
    pass


def load_snapshots(path: str):
    # For every file in the folder
    # append a key of the date with the values of all contents within the file
    # return the dictionary
    directory = os.fsencode(csv_folder_path)
    data = {}


    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"): 
            content = pd.read_csv(f'src\data\\formatted_csv_files\{filename}', index_col=0)
            # print(f"{filename}:\n\t{data}")
            label = re.findall(r'\d+', filename)[0]
            year = int(label[:4])
            month = int(label[4:6])
            day = int(label[6:])
            date = datetime.date(year, month, day)

            data[f"{date.year}-{date.month}-{date.day}"] = content
            print(f"[INFO] Loaded content for {filename}.")
            continue
        else:
            continue
    print(f"[SUCCESS] Completed loading all data from {directory}")
    return data


main()