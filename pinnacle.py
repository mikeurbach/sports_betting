import datetime
import time
import re

from website import Website

class Pinnacle:
    def __init__(self, url, params, headers, cnx, cursor):
        self.url = url
        self.params = params
        self.headers = headers
        self.cnx = cnx
        self.cursor = cursor
        self.website = Website(url, headers, params, cursor, cnx)

    def parse(self):
        print 'parsing:', str(self)

        # get the webpage soup
        soup = self.website.soup()

        # the datatables
        tables = soup.find_all('table', class_='linesTbl')

        # slurp up rows (they come in groups of three)
        gamerows = {}
        for table in tables:
            # get the date for this table
            datestr = table.select('.linesHeader')[0].find('h4').text
            match = re.search('(\d{0,1})/(\d{2})', datestr)
            month = int(match.group(1))
            day = int(match.group(2))
            date = datetime.date(2015, month, day)
            gamerows[date] = []

            # sigh, go through all colors of table
            for row in table.select('.linesAlt1'):
                gamerows[date].append(row)
            for row in table.select('.linesAlt2'):
                gamerows[date].append(row)

        # group rows into 3 tuples
        # http://code.activestate.com/recipes/303060-group-a-list-into-sequential-n-tuples/
        gametuples = {}
        for date in gamerows:
            gametuples[date] = []
            for i in range(0, len(gamerows[date]), 3):
                tup = gamerows[date][i:i+3]
                if len(tup) == 3:
                    gametuples[date].append(tuple(tup))

        # go through for times and lines
        lines = []
        for date in gametuples:
            for linerowa, linerowb, draw in gametuples[date]:
                # get the datetime
                timeline = linerowb.select('td')[0].text
                match = re.search('(\d\d):(\d\d) ((A|P)M)', timeline)
                timestr = match.group(0)
                timeobj = datetime.datetime.strptime(timestr, '%I:%M %p').time()
                datetimeobj = datetime.datetime.combine(date, timeobj)
                
                # get the lines
                lineaname = linerowa.select('.linesTeam')[0].text
                linebname = linerowb.select('.linesTeam')[0].text
                linealine = float(linerowa.select('.linesMLine')[0].text)
                linebline = float(linerowb.select('.linesMLine')[0].text)
                drawline = float(draw.select('.linesMLine')[0].text)
                
                lines.append((lineaname, linealine, linebname, linebline, drawline))

        return lines

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__,
                                 self.website)
