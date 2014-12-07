from game import Game
from team import Team
from odds import Odds

class Scraper:
    def scrape(self, scrape_id):
        # parse the html
        games = self.parse()

        # for each game
        output = {}
        for game in games:
            awayteamstr, awayline, hometeamstr, homeline, gametime = game

            # initialize the teams
            awayteam = Team(awayteamstr, self.cursor, self.cnx)
            hometeam = Team(hometeamstr, self.cursor, self.cnx)

            # initialize the game
            game = Game(gametime, awayteam, hometeam,
                        self.cursor, self.cnx)

            # insert the odds
            odds = Odds(self.website, game, awayline, homeline, scrape_id,
                        self.cursor, self.cnx)

            # save the pair into our output
            output[game._id] = odds.pair()

        return output
