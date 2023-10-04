# natural_language_processing
Collection of scripts used for natural language processing of Tweets, including common word analysis and location mention extraction.

## About
All of these scripts were developed as part of a Thesis project investigating the use of social media, particularly Twitter data, to explore urban gully events in Nigeria.

### tweet_common_words
This script takes a CSV of tweet text as input and performs simple cleaning (removing stopwords and punctuation and converting to lower case) and analysis to determine the most commonly used words.

### location_extraction_final
Takes csv input with two columns, Tweet (text) and Relevance (1-3), produces output table with location names extracted from the tweets. New entry for each unique location name in each tweet. Additionally counts the occurences of each unique location name after grouping by R type.

Workflow: 
    - Setup includes loading and defining punctuation and loading SpaCy model
    - Defines function to use SpaCy NLP entity detection to extract location names, only including each unique location once and excluding punctuation
    - Defines function to process tweets using above function and generate output table 
    - Uses the functions with input file
    - Groups results by relevance types and counts occurrences of unique location names for each group
    - Exports to excel files

### geotag_vs_text_locations
Location name extraction from only geotagged tweets. Retains city and state info from the geotagged data, and adds the GPE extracted from the text. Adds column to show if the GPE is different from the city or state obtained from geotagged data. 
