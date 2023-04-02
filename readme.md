# Web Scraping with BeautifulSoup 
## Scraping the Goodreads Best Romances of 2022 for reviews

### What is this?
Just the start of a project at the moment, so very much a **work in progress for now**. I'm learning how to use BeautifulSoup by scraping through the Goodreads site. It starts on the "Best Romances of 2022" shortlist, navigating through each book and extracting the first 30 reviews. The information that is collected is the following:
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

### What is it for?
This is going to eventually become a pandas dataframe and then a .csv file, which I'll upload to Kaggle and start to use as part of a portfolio project on sentiment analysis

### What skills does this code show?
1. Python: BeautifulSoup and Pandas
2. Web scraping
3. Automated dataset creation