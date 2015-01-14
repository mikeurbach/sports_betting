import json
import importlib
from datetime import datetime

from game import Game
from team import Team
from odds import Odds

# should be pickled
from pinnacle import Pinnacle
class_lookup = {
    'Pinnacle': Pinnacle
}

class Scraper:
    def __init__(self, filename, cnx, cursor):
        self.scrape_id = 1
        self.scrapers = []
        self.cnx = cnx
        self.cursor = cursor

        # create scrapers
        with open(filename) as f:
            for line in f:
                klass, url, params, headers = line.split(',')
                scraper_class = class_lookup[klass]
                url = url
                params = json.loads(params)
                headers = json.loads(headers)
                self.scrapers.append(scraper_class(url, params, headers, cnx, cursor))

        print 'scrapers:', str(self.scrapers)

    def scrape(self):
        timestamp = datetime.now()

        # for each scraper
        output = {}
        for scraper in self.scrapers:
            # parse the html
            games = scraper.parse()

            # for each game
            for game in games:
                awayteamstr, awayline, hometeamstr, homeline, gametime = game

                # initialize the teams
                awayteam = Team(awayteamstr, self.cursor, self.cnx)
                hometeam = Team(hometeamstr, self.cursor, self.cnx)

                # initialize the game
                game = Game(gametime, awayteam, hometeam,
                            self.cursor, self.cnx)

                # insert the odds
                odds = Odds(scraper.website, game, awayline, homeline, self.scrape_id, timestamp, scraper.cursor, scraper.cnx)

                # save the pair into our output
                output[game._id] = odds.pair()

        # increment scrape id
        self.scrape_id += 1

        return output
