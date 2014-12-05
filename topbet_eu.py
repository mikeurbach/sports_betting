import re
from scraper import Scraper
from website import Website
from datetime import time, datetime
from time import strptime, mktime

class TopBetEu(Scraper):
    def __init__(self, url, cnx, cursor, headers={}, params={}):
        self.url = url
        self.cnx = cnx
        self.cursor = cursor
        self.website = Website(url, cursor, cnx,
                               headers=headers, params=params)

    def parse(self):
        # get the webpage soup
        soup = self.website.soup()

        # for each game
        games = []
        for eventdiv in soup.find_all('div', class_='event'):
            # read the game header
            header = eventdiv.find('h3').text

            # read the teams
            match = re.search('(\w.+) at (\w.+) ', header)
            awayteamstr = re.sub('-.+', '', match.group(1)).replace('.', '%')
            hometeamstr = re.sub('-.+', '', match.group(2)).replace('.', '%')

            # read the gametime
            match = re.search('(....)-(..)-(..)\s+(..):(..)', header)
            gametime = datetime(
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3))
            )

            # read the lines
            awaycell, homecell = [line for line in eventdiv.find_all('td', class_='money')]
            awayline = int(awaycell.text)
            homeline = int(homecell.text)

            games.append((
                awayteamstr,
                awayline,
                hometeamstr,
                homeline,
                gametime,
            ))

        return games
