import re
from website import Website
from datetime import time, datetime
from time import strptime, mktime

class SportsBettingAg:
    def __init__(self, url, headers, params, cnx, cursor):
        self.url = url
        self.params = params
        self.headers = headers
        self.cnx = cnx
        self.cursor = cursor
        self.website = Website(url, params, headers, cursor, cnx)

    def parse(self):
        # get the webpage soup
        soup = self.website.soup()

        # the datatable
        table = soup.body.find_all('table')[1]

        # for each game
        games = []
        for tbody in table.find_all('tbody'):
            if tbody.attrs['class'][0] == 'date':
                # keep track of what date we're talking about
                match = re.search('\w, (.+) - NFL Football Game', tbody.find('tr').find('td').text)
                t = strptime(match.group(1), '%b %d, %Y')
                date = datetime.fromtimestamp(mktime(t))
            else:
                # grab the two rows
                awayrow = tbody.find('tr', class_='firstline')
                homerow = tbody.find('tr', class_='otherline')

                # read the two teams
                awayteamstr = awayrow.find('td', class_='col_teamname').text
                hometeamstr = homerow.find('td', class_='col_teamname').text

                # read the two lines
                awaylinestr = awayrow.find('td', class_='moneylineodds').text
                homelinestr = homerow.find('td', class_='moneylineodds').text

                # if they were empty
                if awaylinestr == '' and homelinestr == '':
                    awaylinestr = u'-10000'
                    homelinestr = u'-10000'

                awayline = int(awaylinestr)
                homeline = int(homelinestr)

                games.append((
                    awayteamstr,
                    awayline,
                    hometeamstr,
                    homeline,
                    date,
                ))

        return games

    def __repr__(self):
        return '{0}({1},{2},{3})'.format(self.__class__.__name__,
                                         self.url,
                                         self.params,
                                         self.headers)
