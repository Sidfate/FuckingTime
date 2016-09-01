import requests
from lxml import etree
import sqlite3
from tools.public import *

url = 'http://wufazhuce.com/'
html = requests.get(url).content.decode('utf-8')
selector = etree.HTML(html)

url = selector.xpath('//div[@class="carousel-inner"]/div[@class="item active"]/a/img/@src')
text = selector.xpath('//div[@class="carousel-inner"]/div[@class="item active"]/div[@class="fp-one-cita-wrapper"]/div[@class="fp-one-cita"]/a/text()')

conn = getSqlCur()
cur = conn.cursor()
selects = cur.execute("SELECT * FROM article WHERE date=?", (getToday(),))
if selects.fetchone() is None:
    cur.execute("INSERT INTO article VALUES ('"+getToday()+"','"+url[0]+"', '"+text[0]+"')")
endSqlCur(cur, conn)