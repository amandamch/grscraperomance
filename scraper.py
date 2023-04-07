from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd

# This is creating a small dataset using the first page of reviews (30 per book)
# The aim is more to prove I can use the tool and conduct sentiment analysis, rather than creating a dataset with 17000+ reviews per book

romances = requests.get("https://www.goodreads.com/choiceawards/best-romance-books-2022").text
soup = BeautifulSoup(romances, 'lxml')

# Find and collect the URLs of the books that were nominated
links = []
books = soup.findAll("a", class_="pollAnswer__bookLink")
for book in books:
    link = str("https://www.goodreads.com" + str(book['href']))
    links.append(link)

# Creating lists to add the information to, to eventually make into dicts to make into a pandas dataframe
book_id = []
book_title = []
book_author = []
review_id = []
review_date = []
review_writer = []
review_rating = []
review_text = []

# Creating values to increment for books and review id
bookid = 0
reviewid = 0

# Iterate through each page for each book, and collect information from the reviews on each
for link in links:
    booklink = requests.get(link).text
    reviewfinder = BeautifulSoup(booklink, 'lxml')
    if reviewfinder.find("h1", class_="Text Text__title1"):
        booktitle = reviewfinder.find("h1", class_="Text Text__title1").text
    bookauthor = reviewfinder.find("span", class_="ContributorLink__name").text
    reviews = reviewfinder.findAll("section", class_="ReviewText__content") # This is the closest class level that is not in common with the blurb

    for review in reviews:
        review = review.div.div.span.get_text() # Go into the truncatedcontent divs and pull out the text stripped of formatting tags
        review_text.append(review)
    # TODO: Strip and clean the text here, and then we can add it into a dataframe at a later point

    # This one gets the reviewers sorted, as well as the things that don't need finding for every single link, like the book title and author, and book id / review id 
    reviewers = reviewfinder.findAll("div", class_="ReviewerProfile__name")
    for person in reviewers:
        reviewer = person.a.string
        review_writer.append(reviewer)
        review_id.append(reviewid)
        book_id.append(bookid)
        reviewid += 1
        book_title.append(booktitle)
        book_author.append(bookauthor)

    reviewdate = reviewfinder.findAll("span", class_="Text Text__body3") # Finding all review dates
    for date in reviewdate:
        # The first of this class on every page won't because the span class "Text Text__body3" also covers the publication date info at the top of the page
        dateofreview = date.a
        # If we're not looking at the top of the page publication info, we get the review date as a link, so we can extract the text from that
        # We then convert to datetime so we can actually use the data
        if dateofreview != None:
            dateofreview = date.a.string
            datefinal = datetime.strptime(dateofreview, "%B %d, %Y").date()
            review_date.append(datefinal)

    allcards = reviewfinder.findAll("div", class_="ShelfStatus") # Looking through review cards for rating
    for card in allcards:
        # Making sure 'None' is added into the reviews that provided no rating
        if card.text == "Read" or card.text == "Want to read" or "Shelved as" in card.text:
            review_rating.append("None")
        elif card.find("span", class_="RatingStars RatingStars__small"):
            # If we have a rating (and thus rating stars), we extract the rating in the form of the aria-label and index the text for the number
            # All ratings were formatted as "Rating x out of 5" so the rating number could be reliably found from the string
            rating = card.find("span", class_="RatingStars RatingStars__small")["aria-label"]
            review_rating.append(rating[7])
    
    bookid += 1

# We've now done the scraping and turning the data into something usable, so the next step is creating a pandas dataframe
# This is really easy; we just create a dictionary of the lists that we've constructed
# Since we've accounted for all the None reviews, all the lists are the same length and line up

dict = {'book_id': book_id, 
        'book_title': book_title,
        'book_author': book_author,
        'review_id': review_id,
        'review_date': review_date,
        'review_writer': review_writer,
        'rating': review_rating,
        'review_text': review_text}

df = pd.DataFrame(dict)

df.to_csv('scraped.csv')