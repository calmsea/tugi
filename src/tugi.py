#!/usr/bin/env python

import member
from datatype import * 

def test():
    gen = member.Generator()
    gen.data = [
            'http://www.rssnavi.jp/rss/?k=caterss8',
            'http://journal.mycom.co.jp/haishin/rss/index.rdf',
            String('http://www.google.com/reader/public/atom/user%2F00031631171024228684%2Fstate%2Fcom.google%2Fbroadcast'),]

    ms = []
    ms.append(gen)
#    ms.append(member.SubElement())
    ms.append(member.Str2Url())
    ms.append(member.FetchFeed())
    ms.append(member.OutputHTML())
    for m in zip(ms[:-1], ms[1:]):
#        print m
#        print "m[0].join(m[1])"
        m[0].join(m[1])
    m[-1].run()

if __name__ == '__main__':
    test()

#
# EOF
#
