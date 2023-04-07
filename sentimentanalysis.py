import spacy
import nltk
import pandas as pd
import re
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

#nltk.download('punkt')
#nltk.download('stopwords')

# Create instance of spaCy parser
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# Get the csv file that we had and read it as a dataframe
df = pd.read_csv('scraped.csv')
df = df[df['rating'].notna()] # Removing rows from the dataframe where the review value is null- from 600 to 562 rows; doing it here saves them from being preprocessed unnecessarily

# The first thing that we can do with the data is explore what it looks like
# Here, it's useful particularly to know the number of reviews with each star rating
# If we're going to split into positive and negative reviews, we might want to decide whether 3 star reviews are more useful as negative than positive
onestar = 0
twostar = 0
threestar = 0
fourstar = 0
fivestar = 0
posneg = [] # creating a binary split between positive and negative, rather than just star ratings

for review in range(len(df)):
    if df.iloc[review]['rating'] == 1:
        onestar += 1
        posneg.append(0)
    elif df.iloc[review]['rating'] == 2:
        twostar += 1
        posneg.append(0)
    elif df.iloc[review]['rating'] == 3:
        threestar += 1
        posneg.append(0)
    elif df.iloc[review]['rating'] == 4:
        fourstar += 1
        posneg.append(1)
    else:
        fivestar += 1
        posneg.append(1)

print(f" One star reviews: {onestar} \n Two star reviews: {twostar} \n Three star reviews: {threestar} \n Four star reviews: {fourstar} \n Five star reviews: {fivestar} \n Total reviews: {len(df['rating'])}")

# This preliminary investigation shows us that there are 55, 88, 82, 152, and 185 of each star rating respectively, out of 562 reviews
# If we count 3 star reviews as negative, we have a roughly 60-40 positive-negative split, which is a better balance than if we counted 3 star reviews as positive
# This have been added into the code above, and gets added to the dataframe here:
df['posneg'] = posneg

# Tokenise the data - need to figure out how to do this for every review in the dataframe
def preprocessing(review):
    words = [token.lemma_ for token in nlp(review) if not token.is_punct] # Tokenizing and lemmatizing (rather than stemming, to ensure more correct word forms)
    words = [re.sub(r"[^A-Za-z@']", "", word) for word in words] # Use regex to replace the characters that are not A-Za-z@' with nothing, including emoji
    words = [re.sub(r"\S+(com|co.uk|net+\S)", "", word) for word in words] # Removing websites
    words = [word for word in words if word != ' ' and word != ''] # Removing empty and empty words if there are any left
    stopwords = nltk.corpus.stopwords.words('english') # Importing NLTK stopwords
    words = [word.lower() for word in words if word.lower() not in stopwords] # Removing stopwords from text
    review_stemmed = " ".join(words) # Returning strings so that we can create a corpus of text
    return review_stemmed

df['reviews_cleaned'] = df['review_text'].apply(preprocessing)
text = df['reviews_cleaned']

# Vectorise the cleaned documents in the corpus- here using TF/IDF over Bag of Words, to minimise potential matrix sparsity
# The TF/IDF approach also tends to work better than BoW in machine learning, which is the aim here
# The preliminary concern with the sentiment classification here is data sparsity generally as we only have 562 reviews, but we'll see!

vectorizer = TfidfVectorizer(stop_words='english')
vectorizer.fit(text)
vector = vectorizer.transform(text)

# First trying binary classification using a logistic regression
X_trained, X_tested, y_trained, y_tested = train_test_split(vector, df['posneg'], shuffle=False)
logreg = LogisticRegression(solver='liblinear')
logreg.fit(X_trained, y_trained)

y_pred = logreg.predict(X_tested)
accscore = accuracy_score(y_tested, y_pred)

print("Binary Sentiment Analysis Accuracy: ", accscore)

# Split into train/test for rating star prediction
X_train, X_test, y_train, y_test = train_test_split(vector, df['rating'], shuffle=False) # Without shuffling, accuracy has been as high as 0.45, but we want unshuffled data so our figures are reproducible

# Attempting to classify the data according to the number of stars given in the review, using a logistic regression
lr = LogisticRegression(solver='liblinear') #liblinear solver works better with the data than the default lbfgs
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)
score = accuracy_score(y_test, y_pred)

print("Rating Star Prediction Accuracy: ", score)