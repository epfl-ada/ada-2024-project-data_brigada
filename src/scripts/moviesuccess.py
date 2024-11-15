import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# Define the paths
MOVIE_METADATA_PATH = "../../data/MovieSummaries/movie.metadata.tsv"
OUTPUT_TOP_5_PERCENT_PATH = os.path.join("..", "..", "data", "MovieSummaries", "top_5_percent_movies.tsv")

def load_movie_metadata(file_path):
    """Load movie metadata directly, as the file already contains headers."""
    movies_df = pd.read_csv(file_path, sep='\t')
    return movies_df

def get_top_5_percent_successful_movies(movies_df):
    """Filter the top 5% most successful movies based on box office revenue."""
    top_5_percent_threshold = movies_df["Box office revenue"].quantile(0.95)
    top_5_percent_movies_df = movies_df[movies_df["Box office revenue"] >= top_5_percent_threshold]
    return top_5_percent_movies_df

def drop_old_movies(movies_df, year_threshold=1960):
    """Drop movies released before 1960."""
    movies_df = movies_df[movies_df["Release date"] >= year_threshold]
    return movies_df

def plot_top_5_percent_movies(data):
    """Plots a bar chart of movies by box office revenue."""
    # Sort movies by box office revenue for a cleaner visualization
    data = data.sort_values(by="Box office revenue", ascending=False)

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.bar(data["Name"], data["Box office revenue"])
    plt.xticks(rotation=90)  # Rotate movie names on the x-axis for better readability
    plt.xlabel("Movies")
    plt.ylabel("Box Office Revenue")
    plt.title("Top 5% Movies by Box Office Revenue")
    plt.tight_layout()  # Adjust layout to fit x-axis labels

    plt.show()

# Merge the two dataframes on "Wikipedia movie ID" to get only the characters from top 5% movies
def most_successful_actors(movies, characters):
    """Displays the top actors with the most appearances in the top 5% movies."""
    top_5_movies_with_characters = pd.merge(movies,
                                            characters,
                                            on="Wikipedia movie ID")

    # Count the number of appearances for each actor in the top 5% movies
    actor_counts = top_5_movies_with_characters["Actor name"].value_counts().reset_index()
    actor_counts.columns = ["Actor name", "Appearances in Top 5% Movies"]
    return actor_counts

def actors_avg_revenue(movies, characters, actors):
    """Displays the average box office revenue for movies in which each actor appeared."""
    merged_data = pd.merge(movies, characters, on="Wikipedia movie ID")
    # actors names that have appeared in at least 10 of the best movies
    actor_names = actors[actors["Appearances in Top 5% Movies"] >= 10]["Actor name"]                                 
    top_actor_movies = merged_data[merged_data["Actor name"].isin(actor_names)]

    # Calculate the average box office revenue for movies in which each actor appeared
    actor_avg_revenue = top_actor_movies.groupby("Actor name")["Box office revenue"].mean().reset_index()
    actor_avg_revenue.columns = ["Actor name", "Average Revenue with Actor"]
    # sort the actors by average revenue
    actor_avg_revenue = actor_avg_revenue.sort_values(by="Average Revenue with Actor", ascending=False)
    return actor_avg_revenue

def plot_averages(movies, top_actors):
    """
    Plots a histogram of average revenue for 5 randomly selected actors 
    and includes a horizontal line representing the overall average revenue.
    
    Parameters:
        top_actors (pd.DataFrame): A dataframe containing "Actor name", 
                                   "Average Revenue with Actor", and 
                                   the "Overall Average Revenue" value as a column.
    """
    # Extract the overall average revenue from the DataFrame
    overall_average_revenue = movies["Box office revenue"].mean()
    
    # Randomly select 5 actors
    selected_actors = top_actors.sample(n=5, random_state=42)

    
    # Get actor names and their average revenues
    actor_names = selected_actors["Actor name"]
    actor_revenues = selected_actors["Average Revenue with Actor"]
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(actor_names, actor_revenues, color="skyblue")
    
    # Plot the overall average revenue as a horizontal line
    plt.axhline(y=overall_average_revenue, color="red", linestyle="--", label="Overall Average Revenue")
    
    # Add labels and title
    plt.xlabel("Actor Names")
    plt.ylabel("Average Revenue")
    plt.title("Average Revenue of Randomly Selected Top Actors")
    plt.xticks(rotation=45)
    plt.legend()
    
    # Show the plot
    plt.tight_layout()
    plt.show()
    

################ Script for analyzing both (IMDB AND CMU) datasets ################


# Load datasets
def load_data(cmu_path, ratings_path, basics_path):
    cmu_df = pd.read_csv(cmu_path, sep='\t', header=None, names=[
        'Wikipedia_movie_ID', 'Freebase_movie_ID', 'Movie_name', 'Movie_release_date',
        'Movie_box_office_revenue', 'Movie_runtime', 'Movie_languages',
        'Movie_countries', 'Movie_genres'
    ])
    imdb_ratings_df = pd.read_csv(ratings_path, sep='\t')
    imdb_basics_df = pd.read_csv(basics_path, sep='\t')
    imdb_basics_df = imdb_basics_df[imdb_basics_df['titleType'] == 'movie']
    return cmu_df, imdb_ratings_df, imdb_basics_df

# Merge datasets and clean up
def merge_data(cmu_df, imdb_ratings_df, imdb_basics_df):
    cmu_df['Movie_name'] = cmu_df['Movie_name'].str.lower()
    imdb_basics_df['primaryTitle'] = imdb_basics_df['primaryTitle'].str.lower()
    imdb_movie_ratings_df = pd.merge(imdb_basics_df, imdb_ratings_df, on='tconst', how='inner')
    merged_df = pd.merge(cmu_df, imdb_movie_ratings_df,
                         left_on=['Movie_name', 'Movie_release_date'],
                         right_on=['primaryTitle', 'startYear'],
                         how='inner')
    return merged_df

# Filter and prepare the final dataframe for analysis
def prepare_final_df(merged_df):
    final_df = merged_df[['Movie_name', 'Movie_box_office_revenue', 'averageRating']].dropna()
    final_df['Movie_box_office_revenue'] = pd.to_numeric(final_df['Movie_box_office_revenue'], errors='coerce')
    final_df.dropna(subset=['Movie_box_office_revenue', 'averageRating'], inplace=True)
    return final_df

# Calculate and print correlation
def calculate_correlation(final_df):
    correlation = final_df['Movie_box_office_revenue'].corr(final_df['averageRating'])
    print(f"Correlation between box office revenue and IMDb rating: {correlation}")

# Plot correlation scatter plot
def plot_revenue_vs_rating(final_df):
    # Scatter plot with linear regression line
    plt.figure(figsize=(10, 6))
    sns.regplot(x='averageRating', y='Movie_box_office_revenue', data=final_df, scatter_kws={'alpha': 0.3}, line_kws={"color": "red"})
    plt.title('Box Office Revenue vs IMDb Rating (With Trendline)')
    plt.xlabel('IMDb Rating')
    plt.ylabel('Box Office Revenue')
    plt.yscale('linear')  # Keeping it linear for initial comparison
    plt.show()

    # Heatmap (2D Histogram) of revenue and rating distributions
    plt.figure(figsize=(10, 6))
    plt.hist2d(final_df['averageRating'], np.log1p(final_df['Movie_box_office_revenue']), bins=(30, 30), cmap='Blues')
    plt.colorbar(label='Density')
    plt.xlabel('IMDb Rating')
    plt.ylabel('Log of Box Office Revenue')
    plt.title('2D Histogram of IMDb Rating vs Log of Box Office Revenue')
    plt.show()

# Plot distribution histograms
def plot_distributions(final_df):
    sns.histplot(final_df['Movie_box_office_revenue'], bins=30, kde=True)
    plt.title('Distribution of Box Office Revenue')
    plt.xlabel('Box Office Revenue')
    plt.ylabel('Frequency')
    plt.show()

    sns.histplot(final_df['averageRating'], bins=20, kde=True)
    plt.title('Distribution of IMDb Ratings')
    plt.xlabel('IMDb Rating')
    plt.ylabel('Frequency')
    plt.show()

# Plot top 10 genres by average rating and frequency
def plot_top_genres(genre_df):
    avg_rating_by_genre = genre_df.groupby('Movie_genres')['averageRating'].mean().sort_values(ascending=False).head(10)
    avg_rating_by_genre.plot(kind='bar', title='Top 10 Genres by Average IMDb Rating')
    plt.xlabel('Genre')
    plt.ylabel('Average IMDb Rating')
    plt.show()

    genre_counts = genre_df['Movie_genres'].value_counts().head(10)
    genre_counts.plot(kind='bar', title='Top 10 Most Frequent Genres')
    plt.xlabel('Genre')
    plt.ylabel('Frequency')
    plt.show()

# Plot top 10 highest-grossing movies
def plot_top_revenue_movies(final_df):
    top_10_revenue = final_df.nlargest(10, 'Movie_box_office_revenue')
    top_10_revenue.plot(kind='bar', x='Movie_name', y='Movie_box_office_revenue', title='Top 10 Highest-Grossing Movies')
    plt.xlabel('Movie')
    plt.ylabel('Box Office Revenue')
    plt.show()

# Plot trends over time
def plot_trends_over_time(merged_df):
    merged_df['Movie_release_date'] = pd.to_datetime(merged_df['Movie_release_date'], errors='coerce')
    merged_df['release_year'] = merged_df['Movie_release_date'].dt.year

    avg_revenue_by_year = merged_df.groupby('release_year')['Movie_box_office_revenue'].mean()
    avg_rating_by_year = merged_df.groupby('release_year')['averageRating'].mean()

    avg_revenue_by_year.plot(title='Average Box Office Revenue Over Time')
    plt.xlabel('Year')
    plt.ylabel('Average Box Office Revenue')
    plt.show()

    avg_rating_by_year.plot(title='Average IMDb Rating Over Time')
    plt.xlabel('Year')
    plt.ylabel('Average IMDb Rating')
    plt.show()

