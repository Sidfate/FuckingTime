import time
import sqlite3

def getToday():
    return time.strftime("%Y-%m-%d")

def getSqlCur():
    return sqlite3.connect('data/data.db')

def endSqlCur(cur, conn):
    cur.close()
    conn.commit()
    conn.close()
