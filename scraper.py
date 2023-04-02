from bs4 import BeautifulSoup
import requests

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
    booktitle = reviewfinder.find("h1", class_="Text Text__title1").text
    bookauthor = reviewfinder.find("span", class_="ContributorLink__name").text
    reviews = reviewfinder.findAll("span", class_="Formatted")
    # TODO: Strip and clean the text here, and then we can add it into a dataframe at a later point
    reviewers = reviewfinder.findAll("div", class_="ReviewerProfile__name")
    for person in reviewers:
        reviewer = person.a.string
        review_id.append(reviewid)
        book_id.append(bookid)
        reviewid += 1
        book_title.append(booktitle)
        book_author.append(bookauthor)
    bookid += 1

