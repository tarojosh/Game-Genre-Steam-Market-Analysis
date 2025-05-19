import pickle
import json
from datetime import datetime
import sys

raw_data_path = 'src\data\\raw'
clean_data_path = 'src\data\clean'
category = 'topsellers'


def main():
    # Get the scraped data
    current_date = datetime.now().strftime('%Y%m%d')
    get_file = f'{raw_data_path}\{category}_{current_date}.pkl'

    data = read_pickle_data(get_file)
    print(f"[INFO] Obtained data with {len(data)} titles.")

    # Clean data to be only what we find important
    clean_data = get_clean_data(data)

    # Write the clean data to a json file
    output_file_path = f'{clean_data_path}\{category}_{current_date}.json'
    try:
        with open(output_file_path, 'w') as f:
            json.dump(clean_data, f, indent=2)
            print(f"[SUCCESS] Wrote clean data to \'{output_file_path}\' for {len(clean_data)} titles.")
    except Exception as e:
        print(f"[ERROR] {e}")


def read_pickle_data(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        return data
    except Exception as e:
        print(f"[ERROR] Unable to open file path \'{filepath}\'. {e}")
        sys.exit(0)


# CLEANING THE DATA -------------------------------- #
def get_clean_data(data: list) -> dict:
    """
    The original pkl data contains a lot of information that isn't necessarily important for finding what 
    makes a game popular (such as the description), so this function only takes relevant information
    and returns a new dictionary.
    """
    new_data: dict = {}

    for i in range(len(data)):
        try:
            steam_appid = data[i]['appdetail']['data']['steam_appid']
            name = data[i]['name']
            developers = data[i]['appdetail']['data']['developers']  # There can be multiple, store as array
            publishers = data[i]['appdetail']['data']['publishers']  # There can be multiple, store as array
            currency = _convert_hkd_to_usd(data[i]['appdetail']['data']['price_overview']['initial'])  # Convert this to USD later
            platforms = data[i]['appdetail']['data']['platforms']
            categories = _get_descriptions(data[i]['appdetail']['data']['categories'])
            genres = _get_descriptions(data[i]['appdetail']['data']['genres'])
            release_date = data[i]['appdetail']['data']['release_date']['date']

            new_data[steam_appid] = {
                'name': name,
                'developers': developers,
                'publishers': publishers,
                'currency': currency,
                'platforms': platforms,
                'categories': categories,
                'genres': genres,
                'release_date': release_date,
            }
        except KeyError as e:
            print(f"[WARNING]: Unable to get key {e} from \'{data[i]['name']}\'. Excluding that title from the list of clean data.")
            continue
    
    print("[INFO] Returned clean data.")
    return new_data


def _get_descriptions(content: dict) -> list:
    output: list = []
    
    for tag in content:
        output.append(tag.get('description', 'None'))

    return output


def _convert_hkd_to_usd(hkd: int):
    # TODO: Instead of getting the exact amount of money, make it a price bucket.
    #       This makes sorting data easier as you can just group multiple titles in "Under $5", "$5-$10", "$10-$20", etc.
    usd_estimate = (hkd / 100) * 0.13
    if usd_estimate < 5.0:
        return "Less than $5"
    elif usd_estimate < 10.0:
        return "$5-$10" 
    elif usd_estimate < 20.0:
        return "$10-$20" 
    elif usd_estimate < 30.0:
        return "$20-$30" 
    elif usd_estimate < 40.0:
        return "$30-$40" 
    elif usd_estimate < 50.0:
        return "$40-$50" 
    elif usd_estimate < 60.0:
        return "$50-$60" 
    else:
        return "More than $60" 


if __name__ == '__main__':
    main()