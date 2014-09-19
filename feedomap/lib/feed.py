import feedparser

from feedomap.lib import CACHE

feedparser.PREFERRED_XML_PARSERS.remove('drv_libxml2')

class Feed(object):
    
    def __init__(self, name, feedurl, sender):
        self.name = name
        self.feedurl = feedurl
        self.sender = sender
    
    def parse_feed(self):
        self.cached_entries = CACHE.get_feed_cache(self.name)
        contents = feedparser.parse(self.feedurl)
        new_entries = []
        for item in contents.entries:
            if item not in self.cached_entries:
                new_entries.append(item)
        contents['entries'] = new_entries
        self.contents = contents
    
    def new_to_cache(self):
        for entry in self.contents.entries:
            self.cached_entries.append(entry)
        CACHE.set_feed_cache(self.name, self.cached_entries)