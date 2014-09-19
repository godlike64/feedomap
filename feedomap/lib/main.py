from feedomap.lib.config import Config
from feedomap.lib.feed import Feed
from feedomap.lib.imap import IMAPConnection
from concurrent.futures import ThreadPoolExecutor, as_completed


from feedomap.lib import CONFIG

def run():
    feeds = []
    for feeditem in CONFIG.cp.sections():
        feed = Feed(feeditem, CONFIG.cp[feeditem]['url'], CONFIG.cp[feeditem]['sender'])
        feed.parse_feed()
        feeds.append(feed)
        # See if the feed entries have full HTML of the article
        # Yes, entry['content']['value']
    imap = IMAPConnection(CONFIG.cp['DEFAULT']['host'],
                            int(CONFIG.cp['DEFAULT']['port']), 
                            CONFIG.cp['DEFAULT']['username'], 
                            CONFIG.cp['DEFAULT']['password'])
    imap.connect()
    for feed in feeds:
        for entry in feed.contents['entries']:
            imap.store_entry(feed, entry, 
                             CONFIG.cp[feed.name]['folder'])
        feed.new_to_cache()
