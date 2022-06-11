from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import argparse

from feedomap import __title__, __version__, __description__
from feedomap.config import Config
from feedomap.feed import Feed
from feedomap.imap import IMAPConnection
from feedomap import CONFIG


def loglevel_validator(v):
    if v.upper() not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
        raise argparse.ArgumentTypeError(
            "Log level must be a valid Python " + "log level. See -h for details."
        )
    else:
        return v.upper()


def main():
    parser = argparse.ArgumentParser(
        description=f"{__title__} v{__version__}: {__description__}"
    )
    parser.add_argument(
        "-l",
        "--log-level",
        metavar="level",
        type=loglevel_validator,
        default="INFO",
        help=f"Define {__title__}'s log level. Can be any of "
        "Python's standard log levels: CRITICAL, ERROR, "
        "WARNING, INFO, DEBUG.",
    )
    parser.add_argument(
        "-p",
        "--parallel",
        metavar="N",
        type=int,
        default=0,
        help="Use N threads when fetching feeds/" + "storing items.",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Fetch feeds but do not load them into the IMAP server "
        "nor store them in the cache. Useful for debugging.",
    )
    args = parser.parse_args()
    run(args)


def run(args):
    logformat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=args.log_level, format=logformat)
    logger = logging.getLogger(__name__)
    print(f"{__title__} v{__version__} started.")
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
