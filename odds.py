import numpy as np

class Odds:
    def __init__(self, website, game, awayline, homeline, scrape_id, cursor, cnx):
        self.website = website
        self.game = game
        self.awayline = awayline
        self.homeline = homeline
        self.scrape_id = scrape_id

        # append to the database, save the time
        query = '''INSERT INTO odds (site_id, game_id,
                                     home_line, away_line, scrape_id, timestamp)
                   VALUES ({0},{1},
                           {2},{3},{4}, '{5}')'''.format(self.website._id,
                                                         self.game._id,
                                                         self.homeline,
                                                         self.awayline,
                                                         self.scrape_id,
                                                         self.website.timestamp)
        cursor.execute(query)
        cnx.commit()
        self._id = cursor.lastrowid

    def __repr__(self):
        return "Odds({0},{1},{2},{3},{4},{5},{6})".format(self._id,
                                                          self.website._id,
                                                          self.game._id,
                                                          self.homeline,
                                                          self.awayline,
                                                          self.timestamp,
                                                          self.scrape_id)

    def pair(self):
        return np.array([self.awayline, self.homeline])
