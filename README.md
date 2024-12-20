First download the data from the following links: http://www.cs.cmu.edu/~ark/personas/
https://datasets.imdbws.com/
Then unzip the file and place it in the folder named "data". 
### This prevents uploading the data to github

# Evolution of character archetypes : How can our favorite characters drive a movie’s success over the years ?

## Abstract
This project aims to define movie character archetypes based on the CMU Movie dataset. It explores the evolution of these tropes in cinema over the years, with the goal to uncover which characteristics influence a movie's success and if those traits depend on the film's genre. By analyzing trends over decades with a broad dataset of films, we want to study shifts in character representation, and investigate whether the presence, diversity, and development of certain character archetypes directly correlate with critical acclaim and box office performance. How much do characters affect our enjoyment of a film ? Are certain characters necessary for a film to do well ? These are the questions that sparked our curiosity and motivated us to dive into this project. Through data-driven insights, we want to reveal the role characters play in shaping the cinematic experience and contributing to a movie’s popularity and how this changes depending on the time period. 

## Research questions
1. How can we define the different character tropes ? Are there differences between genders?
2. What has been the evolution of these character tropes over the years ?
3. What is considered a "successful" movie ?
4. Does the character's actor/actress influence the movie's success ? Do archetypes affect the movie's success differently depending on the genre ?
5. What characters make a movie successful ?

## Methods

### Data Preprocessing
Preprocessing normalizes movie information and character information so that trends in heroic and villainous portrayal, together with actor roles, can be analyzed over time. Revenue figures were adjusted for inflation to put them on a comparable footing to enable meaningful comparisons of commercial success across years. Other fields, like languages, countries, and genres, were brought into formats easily manipulable. Ethnicity data was mostly missing or in an unusable form using Freebase ID format and thus was supplemented to allow demographic analysis.

### Data Vizualization 
First of all, for a better understanding of the data, it needs to be visualized. We used mostly histograms to show the distribution of character tropes overall and depending on the film genre as well as to know which genres are the most common to simplify the analysis. We also plotted the distribution of the actor gender to have a better idea on how to analyze the tropes when separating based on gender.  

### Word Embeddings
The `tv tropes` dataset is not large enough for us to do a proper significant analysis with it. To enlarge the dataset, the idea is to use an embedding model to encode the plot summaries and the character tropes and compute the cosine similarity between the two. We would choose a similarity threshold and take the most similar embeddings to find tropes in the movie summaries and enlarge the trope counts. However, after doing this, we realized that the cosine similarities were too low to be able to use the results. We had a mean of around 0.3 and when we took only the ones above 0.5, there were only around 50 data points we could add and by looking at them, some were not even correct. We decided to not use this method to not corrupt the dataset and to only use the `tv tropes` dataset that is small but we know is of high quality.

### Character tropes analysis
We used NLP techniques to analyse the character tropes, in order to define the character archetype between female and male. NLP will be used to process the plot summaries in order to extract the key features and cluster similar plots into groups.

### Successful movies
To define a "successful" movie, we analyzed both IMDb ratings and box office revenue. First, we identified the top 5% of movies based on box office revenue, filtering out films released before 1960 to ensure relevance to contemporary trends. We then explored whether high revenue correlated with high ratings by calculating their correlation and visualizing this relationship with scatter plots, including log transformations and heatmaps. Distribution histograms for both metrics revealed that while ratings were normally distributed, revenue was heavily oriented, with only a few blockbusters achieving exceptionally high earnings. Additionally, we examined genres and actor involvement, observing the highest earning genres and identifying top actors by their frequency in the most successful films and their associated revenue averages. This approach helped us understand the factors contributing to both financial and critical success in cinema.


## Additional datasets
To better understand how character archetypes affect movie success, we are using data from IMDb, which includes ratings, votes, genres, and other details. This extra dataset allows us to see how character traits and types relate to success, measured by box office revenue and IMDb ratings. We are using three main files from IMDb:

title.ratings.tsv.gz which provides ratings and vote counts, which help us measure movie success. By combining this with character or movie data, we can see if certain character/movie types tend to get higher ratings or more votes.
title.akas.tsv.gz which contains alternative titles in different regions and languages. We use it to look at regional preferences, seeing if certain character types are more popular in certain areas.
title.basics.tsv.gz which gives basic info like genre and release year, which lets us study how character types and success metrics have changed over time and across genres.

The IMDb data helps us answer our research questions and IMDb ratings and votes allow us to define and measure success as we can look at which movies and characters types, genders, and ages are linked to higher ratings and popularity.

## Contributions

### Analysis

Data cleaning and preprocessing : Jules

Preliminary Graphs/Analysis : Jules

How can we define the different character tropes ? Are there differences between genders? : Laetitia & Nhat Anh

What has been the evolution of these character tropes over the years ? : Nhat Anh

What is considered a "successful" movie ? : 

Does the character's actor/actress influence the movie's success ? Do character archetypes affect the movie's success differently depending on the genre ? : 

What characters make a movie successful ? : 

### Data story

Website layout and Homepage : Laetitia & Nhat Anh

Introduction : Nhat Anh

Dataset : Laetitia

Character tropes : Laetitia & Nhat Anh

Movie's success : (Interactive Graph) Jules / 

Conclusion : 