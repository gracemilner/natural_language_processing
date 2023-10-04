# -*- coding: utf-8 -*-
"""

Author: Grace Milner

General use: 
    Takes csv input with two columns, Tweet (text) and Relevance (1-3), produces output table
    with location names extracted from the tweets. New entry for each unique location name 
    in each tweet.
    
    Additionally counts the occurences of each unique location name after grouping by R type.

Workflow: 
    - Setup includes loading and defining punctuation and loading SpaCy model
    - Defines function to use SpaCy NLP entity detection to extract location names, only including each unique location once and excluding punctuation
    - Defines function to process tweets using above function and generate output table 
    - Uses the functions with input file
    - Groups results by relevance types and counts occurrences of unique location names for each group
    - Exports to excel files

"""

import os
import pandas as pd
import spacy
import string

# Setting working directory
os.chdir("C:\VUB\Thesis\Data\Tweets\Spatial analysis")

# Loading (medium) model
# (can also use small or large if required, found medium best for this application)
nlp = spacy.load('en_core_web_md')

# Defining punctuation
punctuations = string.punctuation

# (Converting punctuation from one string into a list of strings for each separate punctuation mark)
punctuations2 = [x for x in punctuations]
punctuations2.append("™")  # Adding TM punctuation to the list (as it cropped up as a problem in this data)


def extract_location_names(tweet):
    doc = nlp(tweet)
    location_names = []
    for ent in doc.ents:
        if ent.label_ == 'GPE' and not any([x in ent.text for x in punctuations2]):  # if Geopolitical Entity, but not including punctuation mark
            location_name = ent.text
            if location_name not in location_names:
                location_names.append(location_name)
    return location_names


def process_tweets(input_file):
    df = pd.read_csv(input_file)
    processed_tweets = []

    total_tweets = 0
    tweets_with_gpe = 0

    for index, row in df.iterrows():
        tweet = row['Tweet']
        relevance = row['Relevance']
        location_names = extract_location_names(tweet)
        total_tweets += 1
        if len(location_names) > 0:
            tweets_with_gpe += 1
        for location_name in location_names:
            processed_tweet = {
                'Tweet': tweet,
                'Relevance': relevance,
                'Place Name': location_name
            }
            processed_tweets.append(processed_tweet)

    processed_df = pd.DataFrame(processed_tweets)
    return processed_df, total_tweets, tweets_with_gpe


# Using custom functions to process file
input_file = 'not_geotagged_rel.csv'
processed_df, total_tweets, tweets_with_gpe = process_tweets(input_file)

# Export DataFrame to Excel file
#output_file = 'med_model_results.xlsx'
#processed_df.to_excel(output_file, index=False)
#print(f"DataFrame exported to {output_file} successfully.")

# UNIQUE LOCATION COUNTS (per R type)
# ----------------------------------------
# Group processed DataFrame by Relevance and count unique location names within each group
location_counts = processed_df.groupby(['Relevance', 'Place Name']).size().reset_index(name='Count')

# Export location counts DataFrame to Excel file
location_counts_file = 'location_counts.xlsx'
location_counts.to_excel(location_counts_file, index=False)
print(f"Location counts exported to {location_counts_file} successfully.")

# Print total tweet counts
print(f"Total number of input tweets: {total_tweets}")
print(f"Total number of tweets with at least one extracted GPE: {tweets_with_gpe}")
