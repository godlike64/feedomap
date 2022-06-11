from feedomap.config import Config
from feedomap.cache import FeedCache

__version__ = "0.6"
__title__ = "feedomap"
__description__ = "Store your RSS feeds on your IMAP account."
__url__ = "https://github.com/godlike64/feedomap"
__uri__ = __url__
__doc__ = f"{__description__} <{__uri__}>"
__license__ = "GPLv3"
__author__ = "godlike"
__email__ = "godlike64@gmail.com"

CONFIG = Config()
CACHE = FeedCache()
