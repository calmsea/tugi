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

class Url(String):
    type = 'Url'

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
