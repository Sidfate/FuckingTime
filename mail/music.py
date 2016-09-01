import requests
import random
import sqlite3
from tools.public import *

headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
}
payload = {
    'id': '140330894',
    'updateTime': -1
}
url = 'http://music.163.com/api/playlist/detail'

r = requests.get(url, params=payload, headers=headers)
data = r.json()

if data['code'] == 200 and data['result'] is not None:
    tracks = data['result']['tracks']
    mCount = data['result']['trackCount']
    index = random.randint(0, mCount-1)
    track = tracks[index]

    conn = getSqlCur()
    cur = conn.cursor()
    selects = cur.execute("SELECT * FROM music WHERE date=?", (getToday(),))
    if selects.fetchone() is None:
        cur.execute("INSERT INTO music VALUES ('"+getToday()+"','"+track['name']+"', '"+track['artists'][0]['name']+"', '"+track['album']['picUrl']+"', '"+track['mp3Url']+"')")
    endSqlCur(cur, conn)

