from time import mktime

class Game:
    def __init__(self, datetime, teama, teamb, cursor, cnx):
        # away team is one that python lexicographically sorts first
        if teama < teamb:
            self.awayteam = teama
            self.hometeam = teamb
        else:
            self.awayteam = teamb
            self.hometeam = teama

        # look up this game or create it
        query = '''SELECT game_id, date FROM game
                   WHERE date='{0}'
                   AND   away_id={1}
                   AND   home_id={2}
                   LIMIT 1;'''.format(datetime,
                                      self.awayteam._id,
                                      self.hometeam._id)
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            query = '''INSERT INTO game (date, away_id, away_team, home_id, home_team)
                       VALUES ('{0}',{1},'{2}',{3},'{4}')'''.format(datetime,
                                                                    self.awayteam._id,
                                                                    self.awayteam.name,
                                                                    self.hometeam._id,
                                                                    self.hometeam.name)
            cursor.execute(query)
            cnx.commit()
            self._id = cursor.lastrowid
            self.date = datetime
        else:
            self._id = result[0]
            self.date = result[1]
   

    def __repr__(self):
        return "Game({0},{1},{2})".format(self.date,
                                          self.awayteam,
                                          self.hometeam)
    def __eq__(self, other):
        return (self.awayteam._id == other.awayteam._id and
                self.hometeam._id == other.hometeam._id and
                self.date == other.date)

    def __hash__(self):
        return reduce(lambda a,b: a | b, [self.awayteam._id, self.hometeam._id, int(mktime(self.date.timetuple()))])
