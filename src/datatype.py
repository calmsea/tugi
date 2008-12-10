#
#
#
from cgi import escape
from cStringIO import StringIO
from string import Template

class Base(object):
    type = 'Base'
    def to_str(self, content=''):
        if content:
            return "\n".join(str(self), content)
        else:
            return str(self)
    def to_xml(self, content=''):
        tag = self.type.lower()
        if not content:
            content = str(self)
        return "<%(tag)s>%(content)s</%(tag)s>" % locals()

class String(Base, str):
    type = 'String'

import urlparse
class Url(String):
    type = 'Url'
    index = dict(scheme = 0,
                 netloc = 1,
                 path = 2,
                 params = 3,
                 query = 4,
                 fragment = 5,)
    def __init__(self, urlstr):
        super(Url, self).__init__()
        self.url = urlstr
        self.data = list(urlparse.urlparse(urlstr))
    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            pass
        try:
            assert not key.startswith('_')
            return getattr(self.data, key)
        except:
            i = index.get(key, None)
            if i:
                return self.data[i]
            raise AttributeError, "object has no attribute '%s'" % key
    def geturl(self):
        return self.url

class Array(Base, list):
    type = 'Array'
    def to_str(self):
        content = '\n'.join(['%d : %s' % (v) for v in enumerate(self)])
        return super(Array, self).to_str(content)
    def to_xml(self):
        t = Template('<item index="$i">$content</item>')
        content = '\n'.join([t.substitute(dict(i=i,content=c)) for i,c in enumerate(self)]) 
        return super(Array, self).to_xml(content)

class Hash(Base, dict):
    type = 'Hash'
    def to_str(self):
        content = '\n'.join(['%s : %s' % (v) for v in self.items()])
        return super(Hash, self).to_str(content)
    def to_xml(self):
        t = Template('<item key="$key">$val</item>')
        content = '\n'.join([t.substitute(dict(key=key,val=val)) for key,val in self.items()]) 
        return super(Hash, self).to_xml(content)

class Xml(Base):
    type = 'Xml'
    
#
# EOF
#
