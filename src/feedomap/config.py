import os
import configparser
import sys
from collections import OrderedDict

from feedomap.constants import CONFIG_DIR, CONFIG_FILE


class Config(object):
    def __init__(self):
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        if not os.path.exists(CONFIG_FILE):
            self.create_config()

        self.parse_config()

    def create_config(self):
        self.cp = configparser.ConfigParser(dict_type=OrderedDict, allow_no_value=True)
        self.cp["DEFAULT"]["host"] = "example.com"
        self.cp["DEFAULT"]["port"] = "143"
        self.cp["DEFAULT"]["username"] = "john@example.com"
        self.cp["DEFAULT"]["password"] = "secretpassword"
        self.cp["DEFAULT"]["folder"] = "INBOX.Feeds"
        self.cp["DEFAULT"]["sender"] = "feeds@example.com"
        self.cp["DEFAULT"]["use_feed_name_as_folder"] = "no"
        self.cp["DEFAULT"]["use_feed_folder_as_sender"] = "no"
        self.cp["DEFAULT"]["unverified_ssl"] = "no"
        self.cp["Example Feed"] = OrderedDict()
        self.cp["Example Feed"]["url"] = "http://example2.com/rss.xml"
        with open(CONFIG_FILE, "w") as configfile:
            configfile.write(
                "# This is Feedomap's default configuration "
                + "file. It is an example config \n"
                + "# automatically generated due to no config file found.\n"
                + "# Use this file as a guidance to write your definitive "
                + "config.\n# The values shown here will likely not work.\n\n"
            )
            configfile.write(
                "# Values from [DEFAULT] apply to all sections "
                + "unless specifically overridden for each feed.\n"
            )
            configfile.write(
                "# Folder should follow the IMAP syntax, using "
                + "'.' or '/' as separator, depending on the IMAP\n"
                + "# server configuration. It will be automatically created, "
                + "although intermediary folders won't.\n\n"
            )
            self.cp.write(configfile)
            print("Writing default config file at " + CONFIG_FILE)
            sys.exit(1)

    def parse_config(self):
        self.cp = configparser.ConfigParser(dict_type=OrderedDict)
        self.cp.read(CONFIG_FILE)
        for section in self.cp.sections():
            try:
                bytes(section, "ASCII")
            except UnicodeEncodeError:
                if self.cp.getboolean("DEFAULT", "use_feed_name_as_folder"):
                    print("Folder names cannot use non-ASCII characters.")
                    sys.exit(1)
            try:
                bytes(self.cp[section]["folder"], "ASCII")
            except UnicodeEncodeError:
                if self.cp.getboolean("DEFAULT", "use_feed_name_as_folder"):
                    print("Folder names cannot use non-ASCII characters.")
                    sys.exit(1)
