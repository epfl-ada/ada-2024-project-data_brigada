import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import re
import ast

def load_tropes_data():
    # Keep only movie name and character trope
    tv_tropes = pd.read_csv('./data/MovieSummaries/tvtropes.clusters.txt', sep='\t')
    tv_tropes.columns = ['Character trope', 'Movie information']
    # Extract the "id" from the "Movie information" column
    tv_tropes["Name"] = tv_tropes["Movie information"].apply(lambda x: ast.literal_eval(x)["movie"])

    # Create the new DataFrame with the desired structure
    return tv_tropes[["Name", "Character trope"]]

def load_movies_data():
    # keep only movies name and revenue
    movies_metadata = pd.read_csv('./data/clean/movie_metadata_cleaned.csv')
    movies_metadata.head()
    movies_df = movies_metadata[["Name", "Box office revenue"]]
    # drop movies with no revenue
    movies_df.dropna(subset=["Box office revenue"], inplace=True)
    return movies_df

def merge_data(tropes, movies):
    return pd.merge(tropes, movies, on="Name", how="inner")

def stats(merged):
    # Compute basic statistics of revenue by character trope
    return merged.groupby("Character trope")["Box office revenue"].agg(['count', 'mean', 'median', 'std']).sort_values(by='mean', ascending=False)

def plot_avg_revenue(stats):
    # Let's plot the top 20 archetypes by average revenue for a visual comparison
    top_20_archetypes = stats.head(20).sort_values(by='mean', ascending=True)  # sort ascending for easy viewing

    plt.figure(figsize=(10, 8))
    plt.barh(top_20_archetypes.index, top_20_archetypes['mean'])
    plt.xlabel('Average Box Office Revenue')
    plt.title('Top 20 Archetypes by Average Box Office Revenue')
    plt.tight_layout()
    plt.show()

def most_common_archetypes(merged):
    archetype_frequency = merged['Character trope'].value_counts()

    plt.figure(figsize=(10, 6))
    archetype_frequency.head(20).plot(kind='bar')
    plt.title('Top 20 Most Common Archetypes in the Dataset')
    plt.xlabel('Character Trope')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def box_plot(merged):
    # Pick a few archetypes that appear frequently and compare their box office revenues using boxplots:
    archetype_frequency = merged['Character trope'].value_counts()
    selected_archetypes = archetype_frequency.head(6).index.tolist()  # top 6 most common
    subset = merged[merged['Character trope'].isin(selected_archetypes)]

    plt.figure(figsize=(12, 7))
    subset.boxplot(by="Character trope", column="Box office revenue", rot=45)
    plt.title('Box Office Revenue Distribution for Common Archetypes')
    plt.suptitle('')
    plt.xlabel('Character Trope')
    plt.ylabel('Box Office Revenue')
    plt.tight_layout()
    plt.show()

def top_bottom_tier(merged):
    # Divide movies into top 20% and bottom 20% by revenue and see which archetypes are more common in each category:
    # Determine revenue quartiles
    q1 = merged['Box office revenue'].quantile(0.20)
    q3 = merged['Box office revenue'].quantile(0.80)

    top_quarter = merged[merged['Box office revenue'] >= q3]
    bottom_quarter = merged[merged['Box office revenue'] <= q1]

    top_archetypes_freq = top_quarter['Character trope'].value_counts().head(10)
    bottom_archetypes_freq = bottom_quarter['Character trope'].value_counts().head(10)

    # Plot side by side
    fig, axes = plt.subplots(1, 2, figsize=(20,10))
    top_archetypes_freq.plot(kind='bar', ax=axes[0], title='Top 20% Revenue Archetypes')
    bottom_archetypes_freq.plot(kind='bar', ax=axes[1], title='Bottom 20% Revenue Archetypes')

    for ax in axes:
        ax.set_xlabel('Character Trope')
        ax.set_ylabel('Count')
        ax.tick_params(axis='x', rotation=65)

    plt.tight_layout()
    plt.show()