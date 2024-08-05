# Import libraries
import numpy as np
import time
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# nltk.download('all') # -- Only do first time

def preprocess(text):
    # Tokenize (separate words)
    tokenized_text = word_tokenize(text.lower())

    # Remove Stop Words (remove stuff like and, if, or, but, etc.)
    filtered_tokenized = [item for item in tokenized_text if item not in stopwords.words('english')]

    # Lemmatizing (Truncating words to their stem, like jumped --> jump)
    # Choose to lemmatize and not stem because stemming can lead to innaccuracy
    wnl = WordNetLemmatizer()
    filtered_tokenized_lemmatized = [wnl.lemmatize(word) for word in filtered_tokenized]

    processed = ' '.join(filtered_tokenized_lemmatized)

    return processed

def get_sentiment(text):
    model = SentimentIntensityAnalyzer()
    score = model.polarity_scores(text) # Considers punctuation, idioms, etc.
    return score

def analyze(text):
    text = preprocess(text)
    analysis = get_sentiment(text)
    return analysis

