import time
import mysql.connector
from random import normalvariate
from sportsbetting_ag import SportsBettingAg
from topbet_eu import TopBetEu

# initialize the database
cnx = mysql.connector.connect(user='root',
                                   password='Q!w2E#r4',
                                   database='sports_betting')
cursor = cnx.cursor()

# create scrapers
sportsbetting = SportsBettingAg(
    "http://www.sportsbetting.ag/sports/Line/RetrieveLineData",
    cnx,
    cursor,
    headers={
        "user-agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"
    }
)

topbet = TopBetEu(
    'http://topbet.eu/sportsbook/nfl',
    cnx,
    cursor
)
    
    
# scrape forever
scrape_id = 0
while True:
    print "scrape", scrape_id
    sportsbetting.scrape(scrape_id)
    topbet.scrape(scrape_id)
    time.sleep(normalvariate(5, 1))
    scrape_id += 1

cursor.close()
cnx.close()
