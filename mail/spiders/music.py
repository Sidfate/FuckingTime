import sys
sys.path.append('..')

from tools.spider import Spider
from tools.db import DB
from tools.public import *
import random

headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
}
payload = {
    'id': '140330894',
    'updateTime': -1
}
url = 'http://music.163.com/api/playlist/detail'

if __name__ == '__main__':
    spider = Spider()
    data = spider.req(headers=headers, params=payload).crawl(url, pattern='json')

    if data['code'] == 200 and data['result'] is not None:
        tracks = data['result']['tracks']
        mCount = data['result']['trackCount']
        index = random.randint(0, mCount-1)
        track = tracks[index]

        db = DB()
        select = db.one("SELECT * FROM music WHERE date=?", (getToday(),))
        if select is None:
            insertData = (getToday(), track['name'], track['artists'][0]['name'], track['album']['picUrl'], track['mp3Url'])
            db.execute("INSERT INTO music VALUES (?, ?, ?, ?, ?)", insertData)


