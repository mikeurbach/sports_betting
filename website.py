import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Website:
    def __init__(self, url, params, headers, cursor, cnx):
        # look up this website or create it
        query = '''SELECT page_id, url, params, headers FROM page
                   WHERE url='{0}'
                   AND params='{1}'
                   AND headers='{2}';'''.format(url,
                                                params,
                                                headers)
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            query = '''INSERT into page (url, params, headers)
                       VALUES ('{0}','{1}','{2}');'''.format(url,
                                                             params,
                                                             headers)
            cursor.execute(query)
            cnx.commit()
            self._id = cursor.lastrowid
            self.url = url
            self.params = params
            self.headers = headers
        else:
            self._id = result[0]
            self.url = result[1]
            self.params = json.loads(result[2])
            self.headers = json.loads(result[3])

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
