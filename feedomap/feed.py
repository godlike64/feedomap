import feedparser
import logging
import time

from feedomap import CACHE, CONFIG
from feedomap.imap import IMAPConnection
from feedomap.utils import striphtml

feedparser.PREFERRED_XML_PARSERS.remove('drv_libxml2')

class Feed(object):
    
    def __init__(self, name):
        self.name = name
        self.feedurl = CONFIG.cp[self.name]['url']
        if CONFIG.cp[self.name]['use_feed_name_as_folder'] == 'no':
            self.folder = CONFIG.cp[self.name]['folder']
        else:
            self.folder = CONFIG.cp[self.name]['folder'] + '.' + self.name
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
            new_entry = FeedEntry(item, self.name)
            if new_entry not in self.cached_entries:
                new_entries.append(new_entry)
        self.logger.info(self.name + ': found ' + str(len(contents.entries)) + 
                         ' items, ' + str(len(new_entries)) + ' new.')
        self.entries = new_entries
        self.contents = contents
        return self
    
    def new_to_cache(self):
        for entry in self.entries:
            self.cached_entries.append(entry)
        CACHE.set_feed_cache(self.name, self.cached_entries)
        self.logger.info('Saved ' + str(len(self.entries)) + 
                          ' items from "' + self.name + '" to cache.')


class FeedEntry(object):
    
    def __init__(self, entry, feedname):
        self.title = entry['title']
        self.link = entry['link']
        try:
            self.time_published = time.mktime(entry['published_parsed'])
        except KeyError:
            self.time_published = time.mktime(entry['updated_parsed'])
        try:
            self.date_published = time.asctime(entry['published_parsed'])
        except KeyError:
            self.date_published = time.asctime(entry['updated_parsed'])
        try:
            self.summary = entry['content'][0]['value']
        except KeyError:
            try:
                self.summary = entry['summary']
            except KeyError:
                self.summary = ''
        try:
            self.author = entry['author']
        except:
            self.author = feedname
    
    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other): 
        return self.title == other.title and self.author == other.author and \
            self.date_published == other.date_published
