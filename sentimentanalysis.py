import spacy
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
import re

nltk.download('punkt')
nltk.download('stopwords')

# Create instance of spaCy parser
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# Get the csv file that we had and read it as a dataframe
df = pd.read_csv('scraped.csv')

# Tokenise the data - need to figure out how to do this for every review in the dataframe
def preprocessing(review):
    words = [str(token) for token in nlp(review) if not token.is_punct]
    words = [re.sub(r"[^A-Za-z@']", "", word) for word in words] # Use regex to replace the characters that are not A-Za-z@' with nothing, including emoji
    words = [re.sub(r"\S+(com|co.uk|net)", "", word) for word in words] # Removing websites
    words = [word for word in words if word != ' ' and word != ''] # Removing empty space if there is any left
    stopwords = nltk.corpus.stopwords.words('english') # Importing NLTK stopwords
    words = [word.lower() for word in words if word.lower() not in stopwords]

df['reviews_cleaned'] = df['review_text'].apply(preprocessing)