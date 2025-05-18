import pickle
import json

file = "src\data\popularnew_20250515.pkl"
output_path = 'src\data\clean_data.json'


def main():
    # Get the scraped data
    data = read_pickle_data(file)
    print(f"[INFO] Obtained data with {len(data)} titles.")

    # Clean data to be only what we find important
    clean_data = get_clean_data(data)

    # Write the clean data to a json file
    with open(output_path, 'w') as f:
        json.dump(clean_data, f, indent=2)
        print(f"[SUCCESS] Wrote clean data to \'{output_path}\' for {len(clean_data)} titles.")


def read_pickle_data(filepath):
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    return data


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
            product_languages = data[1]['appdetail']['data']['supported_languages']
            # TODO: DO REGEX and NLP stuff for this
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
                'product_languages': product_languages,
                'release_date': release_date,
            }
        except KeyError as e:
            print(f"[ERROR]: Unable to get key {e} from \'{data[i]['name']}\'. Excluding that title from the list of clean data.")
            continue
    
    print("[INFO] Returned clean data.")
    return new_data


def _get_descriptions(content: dict) -> list:
    output: list = []
    
    for tag in content:
        output.append(tag.get('description', 'None'))

    return output


def _convert_hkd_to_usd(hkd: int):
    # TODO: Pricing isn't exactly what the user pays, or even that accurate
    #       (R.E.P.O is $9.99, but this results in $8.58; Helldivers 2 is $39.99, but this results in $40.04)
    #       This isn't a case of it being the actual value of the cut the devs get, this is something to do with this math.
    return (hkd / 100) * 0.13 


if __name__ == '__main__':
    main()