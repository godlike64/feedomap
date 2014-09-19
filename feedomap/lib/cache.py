import shelve
import os

from feedomap.lib.constants import CACHE_DIR

class FeedCache(object):
    def __init__(self):
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

    def get_feed_cache(self, name):
        shelf = shelve.open(CACHE_DIR + name + '.dbm')
        try:
            entries = shelf['entries']
        except KeyError:
            entries = []
        shelf.close()
        return entries

    def set_feed_cache(self, name, entries):
        shelf = shelve.open(CACHE_DIR + name + '.dbm')
        shelf['entries'] = entries
        shelf.close()