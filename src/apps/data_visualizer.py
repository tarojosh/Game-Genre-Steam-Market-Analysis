import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    data = pd.read_csv('src\data\\formatted_csv_files\steam_topsellers_20250528.csv', index_col=0)
    find_top_genres(data)
    # find_most_common_top_prices(data)


def find_top_genres(data):
    x_label = [category for category in data.columns.tolist() if 'genre_' in category]
    x_label_clean = [col.replace('genre_', '').capitalize() for col in x_label]
    y_label = [data[col].sum() for col in x_label]

    genre_counts = list(zip(x_label_clean, y_label))
    genre_counts.sort(key=lambda x: x[1], reverse=True)
    x_label_sorted, y_label_sorted = zip(*genre_counts)

    plt.bar(x_label_sorted, y_label_sorted, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Number of Games")
    plt.title("Total Games per Genre")
    plt.tight_layout()
    plt.show()


def find_most_common_top_prices(data):
    price_counts = data['currency'].value_counts()
    print(price_counts)
    price_counts = price_counts.sort_values(ascending=False)

    plt.bar(price_counts.index, price_counts.values, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Number of Games")
    plt.title("Most Common Price Range")
    plt.tight_layout()
    plt.show()



if __name__ == '__main__':
    main()