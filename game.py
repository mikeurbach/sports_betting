from time import mktime

class Game:
    def __init__(self, datetime, teama, teamb, test, cursor, cnx):
        # away team is one whose name python lexicographically sorts first
        if teama.name < teamb.name:
            self.awayteam = teama
            self.hometeam = teamb
        else:
            self.awayteam = teamb
            self.hometeam = teama

        # look up this game or create it
        query = '''SELECT game_id, date FROM game
                   WHERE date='{0}'
                   AND   away_team='{1}'
                   AND   home_team='{2}'
                   LIMIT 1;'''.format(datetime,
                                      self.awayteam.name.replace("'", "''").encode('utf8', 'ignore'),
                                      self.hometeam.name.replace("'", "''").encode('utf8', 'ignore'))
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            if not test:
                query = '''INSERT INTO game (date, away_id, away_team, home_id, home_team)
                           VALUES ('{0}',{1},'{2}',{3},'{4}')'''.format(datetime,
                                                                        self.awayteam._id,
                                                                        self.awayteam.name.replace("'", "''").encode('utf8', 'ignore'),
                                                                        self.hometeam._id,
                                                                        self.hometeam.name.replace("'", "''").encode('utf8', 'ignore'))
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
        return (self.awayteam.name == other.awayteam.name and
                self.hometeam.name == other.hometeam.name and
                self.date == other.date)

    def __hash__(self):
        return reduce(lambda a, b: a + a ^ b, [stringhash(self.awayteam.name), stringhash(self.hometeam.name), int(mktime(self.date.timetuple()))])


def stringhash(s):
    return reduce(lambda c1, c2: c1 + c1 ^ c2, map(lambda c: ord(c), s))
