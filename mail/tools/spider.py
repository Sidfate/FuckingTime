import requests
import sqlite3
from tools.public import *

class Spider():

    def __init__(self):
        self.headers = {}
        self.params = {}
        pass

    # set request's headers
    def header(self, headers):
        self.headers = headers
        return self

    # set request's params
    def param(self, params):
        self.params = params
        return self

    def req(self, headers, params):
        self.header(headers)
        self.param(params)
        return self

    # run spider and get data by pattern
    def crawl(self, url, pattern='html'):
        response = requests.get(url, headers=self.headers, params=self.params)
        if pattern == 'html':
            self.response = response.content.decode('utf-8')
        elif pattern == 'json':
            self.response = response.json()
        return self.response

    # save data with optional data driven
    def save(self):
        pass
