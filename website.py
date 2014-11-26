import requests
from bs4 import BeautifulSoup

class Website:
    def __init__(self, url, cursor, cnx, headers={}, params={}):
        #self._id = 1 # just until we have more site
        self.url = url
        self.headers = headers
        self.params = params

        # look up this website or create it
        query = '''SELECT id, url FROM websites
                   WHERE url='{0}';'''.format(self.url)
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            query = '''INSERT into websites (url)
                       VALUES ('{0}');'''.format(self.url)
            cursor.execute(query)
            cnx.commit()
            self._id = cursor.lastrowid
            self.url = self.url
        else:
            self._id = result[0]
            self.url = result[1]

    def __repr__(self):
        return "Website({0})".format(self.url)

    def soup(self):
        res = requests.get(self.url, headers=self.headers, params=self.params)
        return BeautifulSoup(res.text)


    def sql(self):
        return 
