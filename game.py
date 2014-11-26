class Game:
    def __init__(self, datetime, awayteam, hometeam, cursor, cnx):
        self.awayteam = awayteam
        self.hometeam = hometeam

        # look up this game or create it
        query = '''SELECT id, time FROM games
                   WHERE time='{0}'
                   AND   away_id={1}
                   AND   home_id={2}
                   LIMIT 1;'''.format(datetime,
                                      self.awayteam._id,
                                      self.hometeam._id)
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            query = '''INSERT INTO games (time, home_id, away_id)
                       VALUES ('{0}',{1},{2})'''.format(datetime,
                                                      self.hometeam._id,
                                                      self.awayteam._id)
            cursor.execute(query)
            cnx.commit()
            self._id = cursor.lastrowid
            self.time = datetime
        else:
            self._id = result[0]
            self.time = result[1]
   

    def __repr__(self):
        return "Game({0},{1},{2})".format(self.time,
                                          self.hometeam,
                                          self.awayteam)
    def sql(self):
        return
