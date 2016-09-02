import sys
sys.path.append('..')

from tools.spider import Spider
from tools.db import DB
from tools.public import *
from conf.global_setting import MYSQL
from lxml import etree
import MySQLdb
import random

def getData():
    global config

    conn = MySQLdb.connect(**MYSQL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movie")
    selects = cursor.fetchall()
    index = random.randint(0, len(selects)-1)
    movieName = selects[index][1]
    movieUrl = selects[index][2]

    spider = Spider()
    html = spider.crawl(movieUrl)
    selector = etree.HTML(html)

    # movie's name
    name = selector.xpath("//div[@id='content']/h1/span/text()")
    name = ' '.join(name)
    # movie's pic
    pic = selector.xpath("//div[@id='mainpic']//img/@src")
    pic = pic[0] if len(pic) == 1 else ""
    # movie's type
    type = selector.xpath("//div[@id='info']/span[@property='v:genre']/text()")
    type = '/'.join(type)
    # movie's score
    score = selector.xpath("//div[@id='interest_sectl']//strong[@class='ll rating_num']/text()")
    score = score[0] if len(score) == 1 else "Unknown"
    # movie's plot
    plot = selector.xpath("//div[@class='related-info']//span[@property='v:summary']/text()")
    plot = '\n'.join(plot)

    cursor.close()
    conn.close()

    return {
        'name' : name,
        'pic'  : pic,
        'type' : type,
        'score': score,
        'plot' : plot,
        'link' : movieUrl
    }

if __name__ == '__main__':
    movie = getData()

    db = DB()
    select = db.one("SELECT * FROM movie WHERE date=?", (getToday(),))
    if select is None:
        insertData = (getToday(), movie['name'], movie['pic'], movie['type'], movie['score'], movie['plot'], movie['link'])
        db.execute("INSERT INTO movie VALUES (?, ?, ?, ?, ?, ?, ?)", insertData)