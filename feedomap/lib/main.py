from feedomap.lib.config import Config
from feedomap.lib.feed import Feed
from feedomap.lib.imap import IMAPConnection

def run():
    cf = Config()
    feeds = []
    for feeditem in cf.cp.sections():
        feed = Feed(cf.cp[feeditem]['url'])
        feed.parse_feed()
        feeds.append(feed)
    imap = IMAPConnection(cf.cp['DEFAULT']['host'],
                            int(cf.cp['DEFAULT']['port']), 
                            cf.cp['DEFAULT']['username'], 
                            cf.cp['DEFAULT']['password'])
    imap.connect()
    for feed in feeds:
        for entry in feed.contents['entries']:
            imap.store_entry(feed.contents['feed'], entry, cf.cp['DEFAULT']['folder'])