class Team:
    def __init__(self, namestr, cursor, cnx):
        # look up this team or create it
        namestr = namestr.strip().replace("'", "''")
        query = '''SELECT * FROM team
                   WHERE team_name='{0}'
                   LIMIT 1'''.format(namestr)
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
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
        return 'Team({0},{1})'.format(self._id, self.name)

    def sql(self):
        return 

