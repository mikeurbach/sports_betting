import numpy as np

class Odds:
    def __init__(self, website, game, awayline, homeline, drawline, scrape_id, timestamp, cursor, cnx):
        self.website = website
        self.game = game
        self.awayline = awayline
        self.homeline = homeline
        self.drawline = drawline
        self.scrape_id = scrape_id

        # append to the database, save the time
        query = '''INSERT INTO money_line (book_id, game_id,
                                           away_line, home_line, draw_line, scrape_id, timestamp)
                   VALUES ({0},{1},
                           {2},{3},{4},{5},'{6}')'''.format(1, # TODO: use the book table
                                                            self.game._id,
                                                            self.awayline,
                                                            self.homeline,
                                                            self.drawline,
                                                            self.scrape_id,
                                                            timestamp)
        cursor.execute(query)
        cnx.commit()
        self._id = cursor.lastrowid

    def __repr__(self):
        return "Odds({0},{1},{2},{3},{4},{5},{6},{7})".format(self._id,
                                                              self.website._id,
                                                              self.game._id,
                                                              self.awayline,
                                                              self.homeline,
                                                              self.drawline,
                                                              self.scrape_id,
                                                              timestamp)

    def lines(self):
        return np.array([self.awayline, self.homeline, self.drawline])
