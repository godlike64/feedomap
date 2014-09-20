import feedparser
import logging

from feedomap.lib import CACHE, CONFIG
from feedomap.lib.imap import IMAPConnection

feedparser.PREFERRED_XML_PARSERS.remove('drv_libxml2')

class Feed(object):
    
    def __init__(self, name):
        self.name = name
        self.feedurl = CONFIG.cp[self.name]['url']
        if CONFIG.cp[self.name]['use_feed_name_as_folder'] == 'no':
            self.folder = CONFIG.cp[self.name]['folder']
        else:
            self.folder = CONFIG.cp['DEFAULT']['folder'] + '.' + self.name
        if CONFIG.cp[self.name]['use_feed_folder_as_sender'] == 'yes':
            sender = self.name.replace(' ', '').lower()
            self.sender = sender + '@' + CONFIG.cp[self.name]['host']
        else:
            self.sender = CONFIG.cp[self.name]['sender']

        self.imap = IMAPConnection(CONFIG.cp[self.name]['host'],
                                   int(CONFIG.cp[self.name]['port']),
                                   CONFIG.cp[self.name]['username'],
                                   CONFIG.cp[self.name]['password'])
        self.logger = logging.getLogger(__name__)

    def parse_feed(self):
        self.logger.info('Parsing feed ' + self.name + '.')
        self.cached_entries = CACHE.get_feed_cache(self.name)
        contents = feedparser.parse(self.feedurl)
        new_entries = []
        for item in contents.entries:
            if item not in self.cached_entries:
                new_entries.append(item)
        self.logger.info(self.name + ': found ' + str(len(contents.entries)) + ' items, ' +
                     str(len(new_entries)) + ' new.')
        contents['entries'] = new_entries
        self.contents = contents
        return self
    
    def new_to_cache(self):
        for entry in self.contents.entries:
            self.cached_entries.append(entry)
        CACHE.set_feed_cache(self.name, self.cached_entries)
        self.logger.info('Saved ' + str(len(self.contents.entries)) + 
                          ' items from "' + self.name + '" to cache.')