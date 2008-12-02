#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#

from datatype import Xml
import feedparser
import netcache
from cStringIO import StringIO 

class RssEntry(Xml):
    type = 'RssEntry'
    def __init__(self, entry):
        self.data = entry
    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            pass
        try:
            assert not key.startswith('_')
            return self.__getitem__(key)
        except:
            raise AttributeError, "object has no attribute '%s'" % key
    def __getitem__(self, key):
        return self.data.__getitem__(key).encode('utf-8')
    
    def to_xml(self):
        sout = StringIO()
        for key in ('title', 'link', 'summary', 'updated'):
            try: val = self[key]
            except KeyError: continue
            sout.write('<%(key)s>%(val)s</%(key)s>' % locals())
        return super(RssEntry, self).to_xml(sout.getvalue())

class Rss(Xml):
    type = 'Rss'
    def __init__(self, url):
        self.url = url
        self.feed = feedparser.parse(netcache.get(url))
    def entries(self):
        for entry in self.feed.entries:
            yield RssEntry(entry)

def test():
    rss = Rss('http://www.google.com/reader/public/atom/user%2F00031631171024228684%2Fstate%2Fcom.google%2Fbroadcast')
    for e in rss.entries():
        print e.title
        print e.to_xml()

if __name__ == '__main__':
    test()

#
# EOF
#