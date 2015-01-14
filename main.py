import time
import mysql.connector

from random import normalvariate
from arbitrage import Arbitrage
from scraper import Scraper

# initialize the database, games, and scraper
cnx = mysql.connector.connect(user='root',
                                   password='Q!w2E#r4',
                                   database='sports_betting')
cursor = cnx.cursor()
scraper = Scraper("sites.csv", "games.csv", cnx, cursor)
    
# scrape forever
while True and scraper.scrape_id < 2:
    print 'scrape:', str(scraper.scrape_id)

    # get lines from each site
    lines = scraper.scrape()
    print 'lines:', str(lines)

    # look for arbitrage
    # arbitrage = Arbitrage(lines)
    # arbitrage.check()

    # chill
    time.sleep(normalvariate(5, 1))

cursor.close()
cnx.close()
