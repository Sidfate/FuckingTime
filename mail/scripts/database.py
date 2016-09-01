import sqlite3

conn = sqlite3.connect('../data/data.db')
cur = conn.cursor()
cur.execute('create table article (date TEXT, pic TEXT, content TEXT)')
cur.execute('create table music (date TEXT, name TEXT, artist TEXT, pic TEXT, link TEXT)')
cur.close()
conn.commit()
conn.close()
