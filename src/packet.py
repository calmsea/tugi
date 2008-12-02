#
#
#

class Packet(object):
    def __init__(self, item=None):
        self.item = item
    def getItem(self, type="str"):
        try:
            return getattr(self, "to_%s" % type)()
        except AttributeError:
            raise
#            raise ValueError
    def to_str(self):
        return self.item.to_str()
    def to_xml(self):
        return "<packet>%s</packet>" % self.item.to_xml()

#
# EOF
#
