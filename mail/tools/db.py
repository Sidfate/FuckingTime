import sys
sys.path.append('..')

from conf.global_setting import DATAPATH
import sqlite3

class DB():

    def __init__(self):
        self.connect(DATAPATH)

    def connect(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

    def execute(self, sql, params=None):
        if params is None:
            return self.cursor.execute(sql)
        else:
            return self.cursor.execute(sql, params)

    def one(self, sql, params=None):
        selects = self.execute(sql, params)
        return selects.fetchone()

    def all(self, sql, params=None):
        selects = self.execute(sql, params)
        return selects.fetchall()

    def __del__(self):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()