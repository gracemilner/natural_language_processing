'''

Author: Grace Milner

General use: 
    Location name extraction from only geotagged tweets. Retains city and state info from the geotagged data, 
    and adds the GPE extracted from the text. 
    
    Adds column to show if the GPE is different from the city or state obtained from geotagged data. 

'''

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


def is_different_from_city_or_state(location_names, city, state):
    for location_name in location_names:
        if location_name.lower() == city.lower() or location_name.lower() == state.lower():
            return False
    return True


def process_tweets(input_file):
    df = pd.read_csv(input_file)
    processed_tweets = []

    total_tweets = 0
    tweets_with_gpe = 0
    tweets_with_different_gpe = 0  # Counter for tweets with different GPE

    for index, row in df.iterrows():
        tweet = row['TEXT']
        relevance = row['REL']
        city = str(row['CITY'])
        state = str(row['STATE'])
        location_names = extract_location_names(tweet)
        total_tweets += 1
        if len(location_names) > 0:
            tweets_with_gpe += 1
            gpe_different = is_different_from_city_or_state(location_names, city, state)
            if gpe_different:
                tweets_with_different_gpe += 1
        else:
            location_names = ['NA']
            gpe_different = False
        processed_tweet = {
            'TEXT': tweet,
            'REL': relevance,
            'CITY': city,
            'STATE': state,
            'GPE_Different': gpe_different
        }
        for i, location_name in enumerate(location_names):
            column_name = f'GPE_{i+1}'
            processed_tweet[column_name] = location_name
        processed_tweets.append(processed_tweet)

    processed_df = pd.DataFrame(processed_tweets)
    
    # Create intermediate DataFrame for counting unique GPEs within each relevance type
    intermediate_df = pd.DataFrame(columns=['REL', 'GPE'])
    for _, row in processed_df.iterrows():
        relevance = row['REL']
        for i in range(1, len(location_names) + 1):
            column_name = f'GPE_{i}'
            gpe = row[column_name]
            if gpe != 'NA':
                intermediate_df = intermediate_df.append({'REL': relevance, 'GPE': gpe}, ignore_index=True)
    
    # Count unique GPEs within each relevance type
    location_counts = intermediate_df.groupby(['REL', 'GPE']).size().reset_index(name='Count')

    return processed_df, total_tweets, tweets_with_gpe, tweets_with_different_gpe, location_counts



# Using custom functions to process file
input_file = 'geotagged_NLP_input.csv'
processed_df, total_tweets, tweets_with_gpe, tweets_with_different_gpe, location_counts = process_tweets(input_file)

# Export DataFrame to Excel file
# output_file = 'geotag_NLP_results3.xlsx'
# processed_df.to_excel(output_file, index=False)
# print(f"DataFrame exported to {output_file} successfully.")

# Print total tweet counts
print(f"Total number of input tweets: {total_tweets}")
print(f"Total number of tweets with at least one extracted GPE: {tweets_with_gpe}")

# Print the count of tweets with different GPE to existing geotagged data
print(f"Total number of tweets with a different GPE: {tweets_with_different_gpe}")

# Export location counts DataFrame to Excel file
location_counts_file = 'geotag_NLP_location_counts3.xlsx'
location_counts.to_excel(location_counts_file, index=False)
print(f"Location counts exported to {location_counts_file} successfully.")
