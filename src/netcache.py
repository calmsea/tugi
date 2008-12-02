#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#

from urllib import urlopen
import feedparser
import sqlite3 as sql
from datetime import datetime, timedelta
import re

__all__ = ['get',]

dbfile = './netcache.db'
con = sql.connect(dbfile)

def createTable():
    con.executescript('''
create table if not exists cache (
    idx integer primary key,
    ctime datetime default CURRENT_TIMESTAMP,
    utime timestamp default CURRENT_TIMESTAMP,
    etime datetime default CURRENT_TIMESTAMP,
    url text NOT NULL UNIQUE,
    data text DEFAULT NULL,
    rawdata text NOT NULL
);
''')

def urlread(url):
    charset = 'sjis'
    f = urlopen(str(url))
    mo = re.search(r'charset=(?P<charset>\S+)', f.headers['Content-Type'], re.IGNORECASE)
    if mo:
        charset = mo.group('charset')
    rawdata = f.read()
    try: rawdata = rawdata.decode(charset)
    except UnicodeDecodeError:
        try: rawdata = rawdata.decode('utf-8')
        except UnicodeDecodeError:
            try: rawdata = rawdata.decode('shift-jis')
            except UnicodeDecodeError:
                try: rawdata = rawdata.decode('euc-jp')
                except UnicodeDecodeError:
                    rawdata = rawdata.decode('iso2022-jp')
        
    return rawdata

def get(url):
    cur = con.cursor()
    cur.execute('select utime, rawdata from cache where url=?', (url,))
    rawdata = ''
    utime = None
    etime = datetime.utcnow()
    for row in cur:
        utime = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        rawdata = row[1]
        if utime < (datetime.utcnow() - timedelta(minutes=5)):
            utime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            rawdata = urlread(url)
            con.execute('update cache set url=?, utime=?, rawdata=? where url=?', (url, utime, rawdata, url))
            con.commit()
    if not utime:
        rawdata = urlread(url)
        cur.execute('insert into cache (url, rawdata) values(?,?)', (url, rawdata))
        con.commit()
    return rawdata.encode('utf-8')

def status():
    for row in con.execute('select url, ctime, utime from cache'):
        print row
    
def test():
    createTable()
    url = 'http://www.google.com/reader/public/atom/user%2F00031631171024228684%2Fstate%2Fcom.google%2Fbroadcast'
    print get(url)
    status()

if __name__ == '__main__':
    test()

#
# EOF
#           