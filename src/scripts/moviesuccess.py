# Run it first (before the moviesuccessplots jupyter notebook)
import pandas as pd
import os

# Define the paths
MOVIE_METADATA_PATH = "../../data/MovieSummaries/movie.metadata.tsv"
OUTPUT_TOP_5_PERCENT_PATH = os.path.join("..", "..", "data", "MovieSummaries", "top_5_percent_movies.tsv")

# Function to load the movie metadata file
def load_movie_metadata(file_path):
    """Load movie metadata directly, as the file already contains headers."""
    movies_df = pd.read_csv(file_path, sep='\t')
    return movies_df

# Task 1: Select top 10% most successful movies by box office revenue
def get_top_5_percent_successful_movies(movies_df):
    """Filter the top 5% most successful movies based on box office revenue."""
    # Convert "Box office revenue" to numeric, handling non-numeric values
    movies_df["Box office revenue"] = pd.to_numeric(movies_df["Box office revenue"], errors='coerce')
    # Drop rows where "Box office revenue" is NaN
    movies_df = movies_df.dropna(subset=["Box office revenue"])
    # Calculate the threshold for the top 5% most successful movies
    top_5_percent_threshold = movies_df["Box office revenue"].quantile(0.95)
    # Filter the movies to include only those in the top 5% by box office revenue
    top_5_percent_movies_df = movies_df[movies_df["Box office revenue"] >= top_5_percent_threshold]
    return top_5_percent_movies_df

# Save top 5% movies to a file
def save_top_5_percent_movies(top_5_percent_movies_df, output_path):
    """Save the top 5% movies to a TSV file."""
    top_5_percent_movies_df.to_csv(output_path, sep='\t', index=False)
    print(f"Top 5% movies saved to {output_path}")

# Main function to execute tasks
def main():
    # Load the movie metadata
    movies_df = load_movie_metadata(MOVIE_METADATA_PATH)
    # Task 1: Get top 10% most successful movies
    top_5_percent_movies_df = get_top_5_percent_successful_movies(movies_df)
    # Save the result to a file
    save_top_5_percent_movies(top_5_percent_movies_df, OUTPUT_TOP_5_PERCENT_PATH)

if __name__ == "__main__":
    main()
