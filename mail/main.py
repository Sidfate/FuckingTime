import sqlite3
from bs4 import BeautifulSoup
from tools.mail import Mail
from tools.public import *

def getData():
    conn = getSqlCur()
    cur = conn.cursor()
    # get article
    selects = cur.execute("SELECT * FROM article WHERE date=?", (getToday(),))
    article = selects.fetchone()
    article = {
        'pic': article[1],
        'content': article[2]
    }
    #get music
    selects = cur.execute("SELECT * FROM music WHERE date=?", (getToday(),))
    music = selects.fetchone()
    music = {
        'name': music[1],
        'artist': music[2],
        'pic': music[3],
        'link': music[4]
    }
    endSqlCur(cur, conn)
    return {
        'article': article,
        'music': music
    }

def createHtml(data):
    html = open('resources/template.html', 'r')
    soup = BeautifulSoup(html, 'lxml')
    # fill article
    article = soup.find("div", class_="article")
    article.img['src'] = data['article']['pic']
    article.p.string = data['article']['content']
    # fill music
    music = soup.find("div", class_="music")
    music.img['src'] = data['music']['pic']
    music.p.string = data['music']['name']+'-'+data['music']['artist']
    music.audio['src'] = data['music']['link']

    return soup

if __name__ == '__main__':
    data = getData()
    html = createHtml(data)

    mail = Mail()
    mail.create(html.prettify())
    mail.send()