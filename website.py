import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Website:
    def __init__(self, url, headers, params, cursor, cnx):
        #self._id = 1 # just until we have more site
        self.url = url.strip()
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
        return "Website({0},{1},{2})".format(self.url,
                                             self.headers,
                                             self.params)

    def soup(self):
        res = requests.get(self.url, headers=self.headers, params=self.params)
        self.timestamp = datetime.now()
        return BeautifulSoup(res.text)


    def sql(self):
        return 
