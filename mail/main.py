# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from tools.mail import Mail
from tools.db import DB
from tools.public import *

def getData():
    db = DB()
    # get article
    article = db.one("SELECT * FROM article WHERE date=?", (getToday(),))
    if article is not None:
        # pic TEXT, content TEXT
        article = {
            'pic': article[1],
            'content': article[2]
        }
    # get music
    music = db.one("SELECT * FROM music WHERE date=?", (getToday(),))
    if music is not None:
        # name TEXT, artist TEXT, pic TEXT, link TEXT
        music = {
            'name': music[1],
            'artist': music[2],
            'pic': music[3],
            'link': music[4]
        }
    # get movie
    movie = db.one("SELECT * FROM movie WHERE date=?", (getToday(),))
    if movie is not None:
        # name TEXT, pic TEXT, type TEXT, score INT, plot TEXT, link TEXT
        movie = {
            'name': movie[1],
            'pic': movie[2],
            'type': movie[3],
            'score': movie[4],
            'plot': movie[5],
            'link': movie[6]
        }

    return {
        'article': article,
        'music': music,
        'movie': movie
    }

def createHtml(data):
    html = open('resources/template.html', 'r')
    soup = BeautifulSoup(html, 'lxml')
    # fill article
    if data['article'] is not None:
        article = soup.find("div", class_="article")
        article.img['src'] = data['article']['pic']
        article.find("p", class_="article_words").string = data['article']['content']
    # fill music
    if data['music'] is not None:
        music = soup.find("div", class_="music")
        music.img['src'] = data['music']['pic']
        music.find("p", class_="music_name").string = data['music']['name']+'-'+data['music']['artist']
        music.audio['src'] = data['music']['link']
    # fill movie
    if data['movie'] is not None:
        movie = soup.find("div", class_="movie")
        movie.img['src'] = data['movie']['pic']
        movie.find("p", class_="movie_name").a['href'] = data['movie']['link']
        movie.find("p", class_="movie_name").a.string = data['movie']['name']
        movie.find("p", class_="movie_type").string = data['movie']['type']
        movie.find("p", class_="movie_brief").string = data['movie']['plot']
        movie.find("p", class_="movie_score").string = "评分："+str(data['movie']['score'])

    return soup

if __name__ == '__main__':
    data = getData()
    html = createHtml(data)

    mail = Mail()
    mail.create(html.prettify())
    mail.send()