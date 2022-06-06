from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from feedomap.config import Config
from feedomap.feed import Feed
from feedomap.imap import IMAPConnection
from feedomap import CONFIG
from feedomap.constants import PROGNAME, VERSION


def run(args):
    logformat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=args.log_level, format=logformat)
    logger = logging.getLogger(__name__)
    print(PROGNAME + " v" + VERSION + " started.")
    if args.dry_run:
        logger.warning(
            f"Running in dry-run mode. Feeds will be parsed but "
            "no action will be taken. Ignore any 'Storing' messages."
        )
    feeds = []
    if args.parallel <= 1:
        for feeditem in CONFIG.cp.sections():
            feed = Feed(feeditem)
            feed.parse_feed()
            feeds.append(feed)
        for feed in feeds:
            if len(feed.entries) > 0:
                logger.info(
                    f"Storing {len(feed.entries)} items "
                    f"from {feed.name} "
                    f"on {feed.imap.host}."
                )
                if not args.dry_run:
                    for entry in feed.entries:
                        feed.imap.store_entry(feed, entry)
                    feed.new_to_cache()
    else:
        logger.warning(
            f"Using {args.parallel} connections for fetching and storing."
            f"This can cause issues on some some IMAP servers."
            f"Use at your own risk!"
        )
        future_data = []
        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            for feeditem in CONFIG.cp.sections():
                feed = Feed(feeditem)
                feeds.append(feed)
            future_data = {executor.submit(feed.parse_feed): feed for feed in feeds}
        for feed in as_completed(future_data):
            pass
        for feed in feeds:
            logger.info(
                f"Storing {len(feed.entries)} items "
                f"from {feed.name} "
                f"on {feed.imap.host}."
            )
            if not args.dry_run:
                with ThreadPoolExecutor(max_workers=args.parallel) as executor:
                    future_data = {
                        executor.submit(feed.imap.store_entry, feed, entry): entry
                        for entry in feed.entries
                    }
                for nothing in as_completed(future_data):
                    pass
