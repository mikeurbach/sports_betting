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
    def __init__(self, sitesfile, gamesfile, cnx, cursor):
        self.scrape_id = 1
        self.scrapers = []
        self.games = {}
        self.cnx = cnx
        self.cursor = cursor

        # create scrapers
        with open(sitesfile) as f:
            for line in f:
                klass, url, params, headers = line.split(',')
                scraper_class = class_lookup[klass]
                url = url
                params = json.loads(params)
                headers = json.loads(headers)
                self.scrapers.append(scraper_class(url, params, headers, cnx, cursor))

        print 'scrapers:', str(self.scrapers)

        # initialize set of games
        with open(gamesfile) as f:
            for line in f:
                datestr, teamastr, teambstr = line.split(',')
                date = datetime.strptime(datestr, '%d-%b').replace(2015)
                teama = Team(teamastr, False, self.cursor, self.cnx)
                teamb = Team(teambstr, False, self.cursor, self.cnx)
                game = Game(date, teama, teamb, False, self.cursor, self.cnx)
                self.games[game] = game

        print 'games:', str(self.games.items())

    def scrape(self):
        timestamp = datetime.now()

        # for each scraper
        output = {}
        for scraper in self.scrapers:
            # parse the html
            games = scraper.parse()

            # for each game
            for game in games:
                teamaname, teamaline, teambname, teambline, drawline, gametime = game
                teama = Team(teamaname, True, self.cursor, self.cnx)
                teamb = Team(teambname, True, self.cursor, self.cnx)

                # look for this game in our set
                testgame = Game(gametime, teama, teamb, True, self.cursor, self.cnx)
                if testgame in self.games:
                    # get the real game, since its _id is needed
                    realgame = self.games[testgame]

                    # teams could have been sorted
                    if realgame.awayteam.name == teamaname:
                        awayline = teamaline
                        homeline = teambline
                    else:
                        awayline = teambline
                        homeline = teamaline

                    # insert the odds
                    odds = Odds(scraper.website, realgame, awayline, homeline, drawline, self.scrape_id, timestamp, scraper.cursor, scraper.cnx)

                    # save the pair into our output
                    # TODO: use the book table
                    output[realgame._id] = odds.lines()

        # increment scrape id
        self.scrape_id += 1

        return output
