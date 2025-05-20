# We're converting the clean data attained from the pickle_file_reader 
# into a csv format for easier data visualization.
import pandas as pd
import json
import sys

all_genres: list = []
all_categories: list = []

def main():
    # NOTE: You'll need to expand this by allowing for multiple files within a directory
    #       if you want to take into account multiple snapshots of data.
    data = get_data('src\data\clean\\topsellers_20250518.json')  

    # Go through genres and categories and append each unique value to the respective list above before adding rows
    build_categories_and_genres(data)

    # Now build a row
    flat_data = [flatten_data(appid, data[appid]) for appid in data]
    
    # And put it in a dataframe
    df = pd.DataFrame(flat_data)
    df.to_csv("steam_games_clean.csv", index=False)


def flatten_data(appid, game):
    row = {
        "appid": appid,
        "name": game['name'],
        "developers": game['developers'][0] if game['developers'] else "",
        "publishers": game['publishers'][0] if game['publishers'] else "",
        "currency": game['currency'],
        "windows": int(game['platforms']['windows']),
        "linux": int(game['platforms']['linux']),
        "mac": int(game['platforms']['mac']),
        "release_date": pd.to_datetime(game["release_date"], errors='coerce').date(),
    }
    for g in all_genres:
        row[f"genre_{g.lower()}"] = int(g in game["genres"])
    for c in all_categories:
        row[f"cat_{c.lower().replace(' ', '_')}"] = int(c in game["categories"])
    return row


def build_categories_and_genres(data: dict):
    global all_genres
    global all_categories

    _genres = []
    _categories = []
    for appid in data.keys():
        _genres += data[appid]['genres']
        _categories += data[appid]['categories']
    
    all_genres = set(_genres)
    all_categories = set(_categories)


def get_data(filepath: str):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(0)


# _get_data('src\data\clean\\topsellers_20250518.json')

if __name__ == '__main__':
    main()