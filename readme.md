# Web Scraping with BeautifulSoup 
## Scraping the Goodreads Best Romances of 2022 for reviews

### What is this?
The start of a project that will look into sentiment analysis of Goodreads reviews. Learned how to use BeautifulSoup by scraping through the Goodreads site. It starts on the "Best Romances of 2022" shortlist, navigating through each book and extracting the first 30 reviews. The information that is collected is the following:

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
The .csv file that has been produced from the scraper has been uploaded to Kaggle (https://www.kaggle.com/datasets/amandamch/goodreads-best-romance-2022) and will be used as the basis for a sentiment analysis project.

### What skills does this code show?
1. Python: BeautifulSoup and Pandas
2. Web scraping
3. Automated dataset creation
