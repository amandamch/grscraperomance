# Web Scraping with BeautifulSoup for Sentiment Analysis
## Scraping the Goodreads Best Romances of 2022 for reviews, to create logistic regression models to predict sentiment and rating

### What is this?
A project that looks into sentiment analysis of Goodreads reviews. Learned how to use BeautifulSoup by scraping through the Goodreads site. It starts on the "Best Romances of 2022" shortlist, navigating through each book and extracting the first 30 reviews. The information that is collected is the following:

**Books**
- book_id (numeric ID (0-19) for the book)
- book_title (Title)
- book_author (Author)

**Reviews**
- review_id (numeric ID (0-599) for the review)
- review_date (date review was written)
- review_writer (reviewer's screen name)
- rating (out of 5)
- review_text (text; cleaned and stripped)

The data is scraped, formatted, and put into the scraped.csv file. The scraped.csv file is then used in sentimentanalysis.py to conduct some sentiment analysis using spaCy/NLTK, and sklearn for logistic regressions.

### What is it for?
The intent of this is just to create a portfolio piece that can demonstrate my ability to conduct logistic regressions, sentiment analysis, web scraping, data cleaning, and text preprocessing. The .csv file that has been produced from the scraper has been uploaded to Kaggle (https://www.kaggle.com/datasets/amandamch/goodreads-best-romance-2022) and can be used for other projects.

### What skills does this code show?
1. Python: BeautifulSoup, Pandas, Sklearn, spaCy, NLTK
2. Web scraping
3. Dataset creation
4. Data cleaning / text preprocessing
5. Sentiment analysis
6. Logistic regression
