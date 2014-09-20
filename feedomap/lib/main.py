from feedomap.lib.config import Config
from feedomap.lib.feed import Feed
from feedomap.lib.imap import IMAPConnection
from concurrent.futures import ThreadPoolExecutor, as_completed


from feedomap.lib import CONFIG

def run():
    feeds = []
    for feeditem in CONFIG.cp.sections():
        feed = Feed(feeditem)
        feeds.append(feed)

    with ThreadPoolExecutor(max_workers=30) as executor:
        future_data = {executor.submit(feed.parse_feed): feed for feed in feeds}

    for nothing in as_completed(future_data):
        pass

    with ThreadPoolExecutor(max_workers=30) as executor:
        for feed in feeds:
            future_data = {executor.submit(feed.imap.store_entry, feed, entry): entry for entry in feed.contents['entries']}
        #future_data = {executor.submit(imap.store_entries, feed): feed for feed in feeds}
    for nothing in as_completed(future_data):
        pass
    for feed in feeds:
        feed.new_to_cache()
