import requests
import pymongo
import re
import os.path
import traceback
from cfg import config
from logger import logger
from bs4 import BeautifulSoup as bsoup

def get_top250():

    # Initializing MongoDB database and collection
    myclient = pymongo.MongoClient(config['mongo_uri'])
    mydb = myclient["imdb"]
    mycol = mydb["top_250"]

    # drop collection values if already exists
    mycol.drop()

    # Creating lists with data fields we want to store
    film = []
    director = []
    year = []
    ratings = []
    votes = []
    exact_ratings = []

    # Get request to obtain html text from website
    try:
        logger.debug("Making HTTP GET request: " + config['website_url'])
        r = requests.get(config['website_url'])
        res = r.text
        logger.debug("Got HTML source, content length = " + str(len(res)))
    except:
        logger.exception("Failed to get HTML source from " + config['top_movies_url'])
        traceback.print_exc()

    soup = bsoup(res, 'html.parser')

    # Optional - if you want to download the html to your disk
    '''with open(os.path.join(config["save_location"], "lb.html"), 'w', encoding="utf-8") as f:
        f.write(res)'''

    tbody = soup.find('tbody', class_="lister-list")

    if not tbody:
        print("Not Found!")
        return

    # Using Regex and BeautifulSoup to get the desired data values
    td_poster = tbody.find_all('td', class_="posterColumn")
    td_title = tbody.find_all('td', class_="titleColumn")
    td_rating = tbody.find_all('td', class_="ratingColumn imdbRating")

    for poster in td_poster:

        d = poster.find('span', {"name": "ir"}).attrs
        value = d["data-value"]

        rating_3decimal = re.findall('.....', value)
        exact_ratings.append(float(rating_3decimal[0]))


    for title in td_title:

        a_tag = title.find('a')

        name_of_film = a_tag.get_text()
        film.append(name_of_film)

        director_name = re.findall('(.+) \(', a_tag['title'])
        director.append(director_name[0])

        span = title.find('span')
        film_year = re.findall('[0-9]+', span.get_text())
        year.append(film_year[0])

    for rating in td_rating:

        strong_tag = rating.find('strong')
        title = strong_tag['title']

        rating_value = re.findall('(.+) based', title)
        ratings.append(float(rating_value[0]))

        votes_with_comma = re.findall('based on ([0-9,]+)', title)
        votes_sans_comma = votes_with_comma[0].split(',')

        vote = ""
        for num in votes_sans_comma:
            vote = vote + num

        votes.append(int(vote))

    # Check if all fields have exactly 250 rows
    if(len(votes) == 250 & len(ratings) == 250 & len(year) == 250 & len(director) == 250 & len(film) == 250 & len(exact_ratings) == 250):
        table_size = 250
        print("Good to Go")

    # Insert the values row by row in MongoDB collection
    for i in range(table_size):

        row_values = {"Film": film[i], "Director": director[i], "Year": year[i], "Rating": ratings[i], "Votes": votes[i], "Mean_Rating": exact_ratings[i]}

        mycol.insert_one(row_values)


if __name__ == "__main__":

    logger.debug('Starting process')

    logger.debug('Getting links in database')

    get_top250()

    logger.debug('Process complete')
