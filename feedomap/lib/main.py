from feedomap.lib.config import Config
from feedomap.lib.feed import Feed
from feedomap.lib.imap import IMAPConnection
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging


from feedomap.lib import CONFIG
from feedomap.lib.constants import PROGNAME, VERSION

def run(log_level):
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)
    print(PROGNAME + ' v' + VERSION + ' started.')
    feeds = []
    for feeditem in CONFIG.cp.sections():
        feed = Feed(feeditem)
        feed.parse_feed()
        feeds.append(feed)

    # Tepmorarily commenting the threading codepaths. Might enable later via option
    #with ThreadPoolExecutor(max_workers=30) as executor:
    #    future_data = {executor.submit(feed.parse_feed): feed for feed in feeds}
    #for nothing in as_completed(future_data):
    #    pass

    #with ThreadPoolExecutor(max_workers=30) as executor:
    #    for feed in feeds:
    #        print(feed.name)
    #        print(len(feed.contents.entries))
    #        print(type(feed.contents['entries']))
    #        future_data = {executor.submit(feed.imap.store_entry, feed, entry): entry for entry in feed.contents['entries']}
    #        future_data = {executor.submit(imap.store_entries, feed): feed for feed in feeds}
    #for nothing in as_completed(future_data):
    #    pass
    
    for feed in feeds:
        logger.info('Storing ' + str(len(feed.contents['entries'])) + ' items' +
                    ' from ' + feed.name + ' on ' + feed.imap.host + '.')
        for entry in feed.contents['entries']:
            feed.imap.store_entry(feed, entry)
