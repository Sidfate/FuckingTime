import sys
sys.path.append('..')

from tools.spider import Spider
from tools.db import DB
from tools.public import *
from lxml import etree

url = 'http://wufazhuce.com/'

if __name__ == '__main__':
    spider = Spider()
    html = spider.crawl(url)

    selector = etree.HTML(html)
    url = selector.xpath('//div[@class="carousel-inner"]/div[@class="item active"]/a/img/@src')
    text = selector.xpath('//div[@class="carousel-inner"]/div[@class="item active"]/div[@class="fp-one-cita-wrapper"]/div[@class="fp-one-cita"]/a/text()')
    url = url[0] if len(url) == 1 else ""
    text = text[0] if len(text) == 1 else ""

    db = DB()
    select = db.one("SELECT * FROM article WHERE date=?", (getToday(),))
    if select is None:
        insertData = (getToday(), url, text)
        db.execute("INSERT INTO article VALUES (?, ?, ?)", insertData)