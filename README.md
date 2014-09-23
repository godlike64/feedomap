feedomap
========

feedomap is a feed expert. It not only aggregates feeds; it uploads them to your IMAP account.

Usage
=====
~~~
usage: feedomap [-h] [-l level] [-p N]

feedomap v0.2: stores your feeds on your IMAP.

optional arguments:
  -h, --help            show this help message and exit
  -l level, --log-level level
                        Define feedomap's log level. Can be any of Python's
                        standard log levels: CRITICAL, ERROR, WARNING, INFO,
                        DEBUG.
  -p N, --parallel N    Use N threads when fetching feeds/storing items.
~~~