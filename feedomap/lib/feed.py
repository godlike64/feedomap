import feedparser

class Feed(object):
    
    def __init__(self, feedurl):
        self.feedurl = feedurl