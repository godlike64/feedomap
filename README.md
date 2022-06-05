feedomap
========

feedomap is a feed expert. It not only aggregates feeds; it uploads them to your IMAP account.

Usage
=====
~~~
usage: feedomap [-h] [-l level] [-p N]

feedomap v0.6: stores your feeds on your IMAP.

optional arguments:
  -h, --help            show this help message and exit
  -l level, --log-level level
                        Define feedomap's log level. Can be any of Python's
                        standard log levels: CRITICAL, ERROR, WARNING, INFO,
                        DEBUG.
  -p N, --parallel N    Use N threads when fetching feeds/storing items.
~~~

Config file
===========

When run for the first time, Feedomap will set up a default (non-working) configuration file:

~~~
# This is Feedomap's default configuration file. It is an example config 
# automatically generated due to no config file found.
# Use this file as a guidance to write your definitive config.
# The values shown here will likely not work.

# Values from [DEFAULT] apply to all sections unless specifically overridden for each feed.
# Folder should follow the IMAP syntax, using '.' or '/' as separator, depending on the IMAP
# server configuration. It will be automatically created, although intermediary folders won't.

[DEFAULT]
host = example.com
port = 143
username = john@example.com
password = secretpassword
folder = INBOX.Feeds
sender = feeds@example.com
use_feed_name_as_folder = no
use_feed_folder_as_sender = no

[Example Feed]
url = http://example2.com/rss.xml
~~~

The syntax is Python's ConfigParser. Most configuration variables are self-explanatory,
except for the following (can be enabled by specifying 'yes'):

* use_feed_name_as_folder: when enabled, feeds will be stored in a folder named
  after the feed name (do not use non-ASCII characters as they are not supported
  by Python's imaplib), as a child of the feed's pre-defined folder (or DEFAULT's)
* use_feed_folder_as_sender: when enabled, the sender will be the feed's name
  (adjusted for compliance with SMTP standards, e.g. no spaces), lowercased, and
  the hostname (after the @) will be the one defined by the host parameter.