import numpy as np

class Odds:
    def __init__(self, website, game, awayline, homeline, cursor, cnx):
        self.website = website
        self.game = game
        self.awayline = awayline
        self.homeline = homeline

        # append to the database, save the time
        query = '''INSERT INTO odds (site_id, game_id,
                                     home_line, away_line, timestamp)
                   VALUES ({0},{1},
                           {2},{3},'{4}')'''.format(self.website._id,
                                                    self.game._id,
                                                    awayline,
                                                    homeline,
                                                    self.website.timestamp)
        cursor.execute(query)
        cnx.commit()
        self._id = cursor.lastrowid

    def __repr__(self):
        return "Odds({0},{1},{2},{3},{4},{5})".format(self._id,
                                                      self.website._id,
                                                      self.game._id,
                                                      self.homeline,
                                                      self.awayline,
                                                      self.timestamp)

    def pair(self):
        c = max(self.awayline, self.homeline)
        d = min(self.awayline, self.homeline)
        return np.array([c, d])
