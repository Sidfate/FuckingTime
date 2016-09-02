import sys
sys.path.append('..')

from tools.db import DB

db = DB()
db.execute('create table article (date TEXT, pic TEXT, content TEXT)')
db.execute('create table music (date TEXT, name TEXT, artist TEXT, pic TEXT, link TEXT)')
db.execute('create table movie (date TEXT, name TEXT, pic TEXT, type TEXT, score INT, plot TEXT, link TEXT)')
