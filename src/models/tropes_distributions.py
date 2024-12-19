import pandas as pd
import matplotlib.pyplot as plt
import ast
import seaborn as sns


def count_tropes(tv_tropes):
    """Count the number of occurrences for each character trope."""
    tropes_count =tv_tropes['Character trope'].value_counts()
    # Convert the Series to a DataFrame
    tropes_count = pd.DataFrame(tropes_count)
    
    return tropes_count.to_string(index=True)


def tropes_count_histogram(tropes_count):
    """Plot a histogram of the number of occurrences for each character trope and sort it."""
    plt.figure(figsize=(18, 8)) 

    # Sort the data
    tropes_count_sorted = tropes_count.sort_values(by='count', ascending=False)

    plt.bar(tropes_count_sorted.index, tropes_count_sorted['count'])

    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlabel("Tropes", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.title("Tropes Count Histogram", fontsize=14)

    plt.tight_layout()
    plt.show()

def tropes_by_decade(tv_tropes, character_metadata):
    """Get the character tropes per decade"""
    
    # Generate a dataframe with the character trope and the movie release year
    tropes_by_year = pd.DataFrame(tv_tropes['Character trope'])
    movie_dates = []
    for movie_info in tv_tropes['Movie information']: # Get the movie release date for each character
        movie_info = ast.literal_eval(movie_info)
        character_id = movie_info['id']
        if character_metadata[character_metadata['Freebase character/actor map ID'] == character_id].empty:
            movie_date = None
        else:
            movie_date = character_metadata[character_metadata['Freebase character/actor map ID'] == character_id]['Release date'].values[0]
        movie_dates.append(movie_date)
    tropes_by_year.insert(1, "Movie release year", movie_dates)
    # Only keep the year
    tropes_by_year['Movie release year'] = [int(str(date)[:4]) if date is not None else None for date in tropes_by_year['Movie release year']]
    # Only keep the movies released from 1960 onwards
    tropes_by_year = tropes_by_year[tropes_by_year['Movie release year'] >= 1960]
    
    # Divide by decade
    tropes_by_year['Decade'] = (tropes_by_year['Movie release year'] // 10) * 10
    
    return tropes_by_year

def tropes_by_decade_histogram(tropes_by_year):
    """Plot the distribution of character tropes over the years for each decade."""
    decade_trope_counts = tropes_by_year.groupby(['Decade', 'Character trope']).size().unstack(fill_value=0)
    
    for decade in decade_trope_counts.index:
        trope_counts = decade_trope_counts.loc[decade][decade_trope_counts.loc[decade] > 0].sort_values(ascending=False) 
        
        plt.figure(figsize=(10, 4))
        trope_counts.plot(kind='bar')
        
        plt.title(f'Character Tropes in {decade}s')
        plt.xlabel('Character Trope')
        plt.ylabel('Count')
        
        plt.tight_layout()
        plt.show()

def tropes_by_gender(tv_tropes, character_metadata):
    """Plot the distribution of character tropes separating by gender"""
    
     # Generate a dataframe with the character trope and the gender of the actor
    tropes_by_gender = pd.DataFrame(tv_tropes['Character trope'])
    actors_gender = []
    for movie_info in tv_tropes['Movie information']:
        movie_info = ast.literal_eval(movie_info)
        character_id = movie_info['id']
        if character_metadata[character_metadata['Freebase character/actor map ID'] == character_id].empty:
            gender = None
        else:
            gender = character_metadata[character_metadata['Freebase character/actor map ID'] == character_id]['Actor gender'].values[0]
        actors_gender.append(gender)
        
    tropes_by_gender.insert(1, "Actor gender", actors_gender)
    
    # Count the number of F and M for each trope
    trope_counts = tropes_by_gender.groupby(['Character trope', 'Actor gender']).size().reset_index(name='Count')

    # Plot a histogram comparing the two
    plt.figure(figsize=(14, 7))
    sns.barplot(x='Character trope', y='Count', hue='Actor gender', data=trope_counts)

    plt.title('Distribution of Male and Female Character Tropes')
    plt.xlabel('Character Trope')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.show()

def tropes_by_gender_count(tv_tropes, character_metadata):
    """Count the number of occurrences of each gender"""
    # Generate a dataframe with the character trope and the gender of the actor
    tropes_by_gender = pd.DataFrame(tv_tropes['Character trope'])
    actors_gender = []
    for movie_info in tv_tropes['Movie information']:
        movie_info = ast.literal_eval(movie_info)
        character_id = movie_info['id']
        if character_metadata[character_metadata['Freebase character/actor map ID'] == character_id].empty:
            gender = None
        else:
            gender = character_metadata[character_metadata['Freebase character/actor map ID'] == character_id]['Actor gender'].values[0]
        actors_gender.append(gender)
        
    tropes_by_gender.insert(1, "Actor gender", actors_gender)
    
    gender_counts = tropes_by_gender['Actor gender'].value_counts()
    gender_counts = gender_counts.rename_axis('Gender').reset_index(name='Count')
    
    return gender_counts

def tropes_by_genre(tv_tropes, movie_metadata):
    """Plot the top 5 Character Tropes for the top 10 genres"""
    # Get the movie genre for each recorded character 
    tropes_by_genre = pd.DataFrame(tv_tropes['Character trope'])
    movie_genre = []
    for movie_info in tv_tropes['Movie information']:
        movie_info = ast.literal_eval(movie_info)
        movie_name = movie_info['movie']
        if movie_metadata[movie_metadata['Name'] == movie_name].empty:
            gender = None
        else:
            genre = movie_metadata[movie_metadata['Name'] == movie_name]['Genres'].values[0]
        movie_genre.append(genre)
        
    tropes_by_genre.insert(1, "Movie genres", movie_genre)
    
    # Convert the 'Movie genres' column from strings to actual lists
    tropes_by_genre['Movie genres'] = tropes_by_genre['Movie genres'].apply(ast.literal_eval)

    # Exploding the genre list to have one genre per row
    tropes_by_genre_exploded = tropes_by_genre.explode('Movie genres')

    # Only keep the top 10 genres
    genres_of_interest = ['Drama', 'Comedy', 'Romance Film', 
                        'Action', 'Thriller', 'World cinema', 
                        'Crime Fiction', 'Horror', 'Indie', 'Documentary']

    # Filter the DataFrame to include only the specified genres
    filtered_tropes_by_genre = tropes_by_genre_exploded[tropes_by_genre_exploded['Movie genres'].isin(genres_of_interest)]

    # Count the occurrences of each trope within each genre
    trope_genre_counts = filtered_tropes_by_genre.groupby(['Movie genres', 'Character trope']).size().reset_index(name='count')

    # Filter to get the top 5 tropes for each genre
    top_10_tropes_per_genre = trope_genre_counts.groupby('Movie genres').apply(
        lambda x: x.nlargest(5, 'count')
    ).reset_index(drop=True)

    # Plotting all genres in subplots
    unique_genres = top_10_tropes_per_genre['Movie genres'].unique()
    num_genres = len(unique_genres)
    cols = 4  # Number of columns in the subplot grid
    rows = (num_genres + cols - 1) // cols  # Calculate rows needed

    fig, axes = plt.subplots(rows, cols, figsize=(15, rows * 5), constrained_layout=True)

    # Flatten axes for easy indexing
    axes = axes.flatten()

    # Plot each genre
    for i, genre in enumerate(unique_genres):
        genre_data = top_10_tropes_per_genre[top_10_tropes_per_genre['Movie genres'] == genre]
        
        ax = axes[i]
        ax.barh(genre_data['Character trope'], genre_data['count'], color='skyblue')
        ax.set_title(f'{genre}')
        ax.set_xlabel('Count')
        ax.set_ylabel('Character Trope')
        ax.invert_yaxis()  # Invert y-axis for better readability

    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Show the plot
    plt.suptitle('Top 5 Character Tropes by Genre', fontsize=14)
    plt.show()