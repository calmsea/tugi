#
#
#
from itertools import *
from packet import Packet
from datatype import *
from rss import Rss

class Member(object):
    "Member"
    def __init__(self):
        self.requires = {}
        self.options = {}

class IMember(Member):
    "Input Member"
    def __init__(self):
        super(IMember, self).__init__()
        self.outputs = {}
        self.distination = None
    def get(self):
        raise StopIteration
    def join(self, dist, name=None):
        if name is None:
            dist.setSource(self)
        else:
            dist.setParam(self, name)
        self.setDistination(dist)
    def setDistination(self, dist):
        self.distination = dist
        
class OMember(Member):
    "Output Member"
    def __init__(self):
        super(OMember, self).__init__()
        self.params = {}
        self.source = None
    def setRequire(self, name, types=None):
        self.requires[name] = types
        self.params.setdefault(name, None)
    def addOption(self, name, types=None):
        self.options[name] = types
        self.params.setdefault(name, None)
    def setParam(self, src, name):
        self.params[name] = src
    def getParam(self, name):
        self.params[name].get().next()
    def setSource(self, src):
        self.source = src

class IOMember(IMember, OMember):
    "Input/Output Member"
    pass

class DOMember(OMember):
    "Determinate Output Member"
    pass

class Generator(IMember):
    def __init__(self):
        super(Generator, self).__init__()
    def get(self):
        data = self.data
        if isinstance(data, list):
            return chain(imap(Packet, data))
        elif isinstance(data, dict):
            return chain(imap(Packet, data.items()))
        elif isinstance(data, str):
            return chain([Packet(data),])
        else:
            raise StopIteration

class Args(IMember):
    def get(self):
        import sys
        pkt = Packet()
        args = map(lambda v: String(v), sys.argv)
        pkt.item = Array(args)
        pkt.item.append(String("aaa"))
        pkt.item.append(Url("http://www.yahoo.co.jp/"))
        return chain([pkt,])

class Function(IOMember, list):
    def get(self):
        for m in self[:-1], self[1:]:
            m[0].join(m[1])
        return chain(self[-1].get())

class Foreach(IOMember):
    def __init__(self):
        super(Foreach, self).__init__()
        self.addRequire(function, (Function,))
    def get(self):
        for pkt in self.source.get():
            seq = pkt.item
            if isinstance(seq, list):
                seq = enumerate(seq)
            elif isinstance(seq, dict):
                seq = seq.items()
            else:
                continue
            func = self.getParam('function')
            gen = Generator(seq)
            gen.join(func)
            res = Array(func.get())
            pkt.result = res

class SubElement(IOMember):
    def get(self):
        for pkt in self.source.get():
            items = pkt.item
            if isinstance(items, Array):
                for item in items:
                    ret = Packet()
                    ret.item = item
                    yield ret
        raise StopIteration

class Str2Url(IOMember):
    def get(self):
        for pkt in self.source.get():
            item = pkt.item
            if isinstance(item, String):
                p = Packet(Url(item))
                print p
                yield p
        raise StopIteration

class FetchFeed(IOMember):
    def __init__(self):
        super(FetchFeed, self).__init__()
    def get(self):
        for pkt in self.source.get():
            url = pkt.item
            print url
            if isinstance(url, Url):
                rss = Rss(url)
                for entry in rss.entries():
                    pkt = Packet()
                    pkt.item = entry
                    print entry.to_xml()
                    yield pkt
        raise StopIteration
                
class OutputConsole(DOMember):
    def __init__(self, type="str"):
        super(OutputConsole, self).__init__()
        self.type = type
        
    def run(self):
        for pkt in self.source.get():
            print pkt.item.to_xml()
#            print pkt.getItem(self.type)

#
# EOF
#
