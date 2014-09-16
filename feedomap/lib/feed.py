import feedparser

feedparser.PREFERRED_XML_PARSERS.remove('drv_libxml2')

class Feed(object):
    
    def __init__(self, feedurl):
        self.feedurl = feedurl
    
    def parse_feed(self):
        self.contents = feedparser.parse(self.feedurl)