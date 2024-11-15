First download the data from the following link: http://www.cs.cmu.edu/~ark/personas/
Then unzip the file and place it in the folder named "data". 
### This prevents uploading the data to github

# Evolution of character archetypes : How can our favorite characters drive a movie’s success over the years ?

## Abstract
This project aims to define movie character archetypes based on the CMU Movie dataset. It explores the evolution of these tropes in cinema over the years, with the goal to uncover which characteristics influence a movie's success and if those traits depend on the film's genre. By analyzing trends over decades with a broad dataset of films, we want to study shifts in character representation, and investigate whether the presence, diversity, and development of certain character archetypes directly correlate with critical acclaim and box office performance. How much do characters affect our enjoyment of a film ? Are certain characters necessary for a film to do well ? These are the questions that sparked our curiosity and motivated us to dive into this project. Through data-driven insights, we want to reveal the role characters play in shaping the cinematic experience and contributing to a movie’s popularity and how this changes depending on the time period. 

## Research questions
1. How can we define the different character tropes ? What is considered a "hero" or "villain" profile ?
2. What has been the evolution of these character tropes over the years ?
3. What is considered a "successful" movie ?
4. What character archetypes make a movie successful ? Does the character's actor/actress influence the movie's success ?
5. Do character archetypes affect the movie's success differently depending on the genre ?

## Methods
We used NLP techniques to analyse the character tropes, in order to define the character archetype between female and male. In the future, NLP will be used to process the plot summaries in order to extract the key features and cluster similar plots into groups.


### Data Preprocessing
Preprocessing normalizes movie information and character information so that trends in heroic and villainous portrayal, together with actor roles, can be analyzed over time. Revenue figures were adjusted for inflation to put them on a comparable footing to enable meaningful comparisons of commercial success across years. Other fields, like languages, countries, and genres, were brought into formats easily manipulable. Ethnicity data was mostly missing or in an unusable form using Freebase ID format and thus was supplemented to allow demographic analysis.

### Data Vizualization 
First of all, for a better understanding of the data, it needs to be visualized. We used mostly histograms to show the distribution of character tropes overall and depending on the film genre as well as to know which genres are the most common to simplify the analysis. We also plotted the distribution of the actor gender to have a better idea on how to analyze the tropes when separating based on gender.  

### Word Embeddings
The `tv tropes` dataset is not large enough for us to do a proper significant analysis with it. To enlarge the dataset, the idea (that would be implemented in Milestone 3) is to use an embedding model (for example Word2Vec or BERT) to encode the plot summaries and the character tropes and compute the cosine similarity between the two. We would choose a similarity threshold and take the most similar embeddings to find tropes in the movie summaries and enlarge the trope counts. 

## Additional datasets

## Timeline and organisation

In the next steps, we will answer the questions: What character archetypes make a movie successful ? Do character archetypes affect a movie’s success depending on the film genre ?

Week 1: Answer all research questions
Week 2: Homework 2
Week 3: Create the datastory based on our research
Week 4: Design the webpage and do the vizualisation
Week 5: Clean the respository, report

Every team member will continue to work on his part in order to answer the problematic.