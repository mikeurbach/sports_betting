class Team:
    def __init__(self, namestr, test, cursor, cnx):
        # look up this team or create it
        namestr = namestr.strip().replace("'", "''")
        query = '''SELECT team_id, team_name FROM team
                   WHERE team_name='{0}'
                   LIMIT 1'''.format(namestr.encode('utf8', 'ignore'))
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            if not test:
                query = '''INSERT INTO team (team_name)
                           VALUES ('{0}')'''.format(namestr)
                cursor.execute(query)
                cnx.commit()
            self._id = cursor.lastrowid
            self.name = namestr
        else:
            self._id = result[0]
            self.name = result[1]

    def __repr__(self):
        return 'Team({0})'.format(self.name.encode('utf8', 'ignore'))

    def sql(self):
        return 

