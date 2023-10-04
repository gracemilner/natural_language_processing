
"""

Author: Grace Milner

This script takes a CSV of tweet text as input and performs simple cleaning (removing stopwords
and punctuation and converting to lower case) and analysis to determine the most commonly used
words. 

"""
import os
import spacy
import spacy.lang.en
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import string
from collections import Counter
import numpy as np

# Defining stopwords and punctuation
stopwords = spacy.lang.en.stop_words.STOP_WORDS
punctuations = string.punctuation

# (converting punctuation from one string into list of strings for each separate punctuation mark)
punctuations2 = [x for x in punctuations]
punctuations2.append("™") #adding TM punctuation to the list (as it cropped up as a problem in this data)

# Setting working directory
os.chdir("C:\VUB\Thesis\Data\Tweets\Common words analysis\Combined")

# Loading data
df = pd.read_csv("R3.csv")

# Loading SpaCy's English NLP model (small version, no word vectors)
nlp = spacy.load('en_core_web_sm')


# Defining function to clean text
    # Only keeps unique tokens(words), so if 'gully' appears multiple times in original tweet, it will only appear once after cleaning
        # (allows calculation of word proportions later on)
    # removes stopwords and punctuation, performs lemmatisation, and converts to lowercase. 
def cleanup_text(docs):
    texts = []
    for doc in docs:
        doc = nlp(doc, disable=['parser', 'ner']) # Disabling unneeded parts of the nlp pipeline
        # Use a set to keep track of unique tokens in the tweet
        unique_tokens = set()
        for tok in doc:
            # Check if the token is a stopword, contains any punctuation, or if the lemmatised version is a pronoun
            if tok.lemma_ != '-PRON-' and tok.text.lower() not in stopwords and not any([x in tok.text for x in punctuations2]):
                # Only add the token to the unique_tokens set if it hasn't been added before in the same tweet
                #   (using the lemmatised version, so word taken back to root e.g. changing, changes, and changed -> change )
                if tok.lemma_.lower().strip() not in unique_tokens:
                    unique_tokens.add(tok.lemma_.lower().strip())
        # Join the unique tokens into a string and append to texts
        tokens = ' '.join(list(unique_tokens))
        texts.append(tokens)
    return pd.Series(texts)

# Converts the tweets into a list format, one list entry for each tweet 
tweet_text = [text for text in df['Tweet']]

# Cleaning tweet text using custom function from above
tweets_clean = cleanup_text(tweet_text)

# Joining all processed tokens into single string separated by a space, 
# then splitting that string into list of individual tokens 
# Creates long list of all tokens individually, so one list entry for each token (word)
tweets_clean = ' '.join(tweets_clean).split()

# Creating counts for the words
tweets_counts = Counter(tweets_clean)

# Selecting the 15 most common words and their respective counts
tweets_common_words = [word[0] for word in tweets_counts.most_common(15)]
tweets_common_counts = [word[1] for word in tweets_counts.most_common(15)]

# Converting the word counts into proportions (for easier comparison)
all_tweets_count = len(tweet_text)
tweets_common_counts_prop = [word/all_tweets_count for word in tweets_common_counts]



# Plotting the results (with absolute counts)
# fig = plt.figure(figsize=(15,6))
# sns.barplot(x=tweets_common_words, y=tweets_common_counts)
# plt.title('Most Common Words in Tweets where Relevance = 3') # Change as required
# plt.xticks(rotation=45)
# plt.savefig(r'R3.png', dpi = 300, bbox_inches="tight")
# plt.show()


#Plotting the results (with proportional counts)
fig = plt.figure(figsize=(15,6))
sns.barplot(x=tweets_common_words, y=tweets_common_counts_prop)
plt.suptitle('15 Most Common Words in R3 Tweets', fontsize = 25) # Change as required
plt.title('Total R3 Tweets = 577', fontsize = 13)
plt.ylabel("Proportion of Tweets containing word", labelpad=15, fontsize = 15)
plt.xticks(rotation=45, fontsize = 14)
plt.yticks(np.arange(0.0, 1.0, 0.1), fontsize=14)
#plt.savefig(r'R3_top15.png', dpi = 300, bbox_inches="tight")
plt.show()















