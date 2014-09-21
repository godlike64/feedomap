import imaplib
#import time
import logging
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from feedomap.utils import striphtml, craft_message

class IMAPConnection(object):
    
    def __init__(self, host, port, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        if self.port == 993:
            connection = imaplib.IMAP4_SSL(host=self.host, port=self.port)
        else:
            connection = imaplib.IMAP4(host=self.host, port=self.port)
            if self.port == 143:
                connection.starttls()
        connection.login(self.username, self.password)
        self.logger.debug('Connected to ' + self.host + ' as ' + 
                          self.username + '.')
        return connection
    
    def store_entry(self, feed, entry):
        connection = self.connect()
        msg = craft_message(self.username, feed.contents['feed'], entry, 
                            feed.sender)
        connection.create('\"' + feed.folder + '\"')
        connection.subscribe('\"' + feed.folder + '\"')
        connection.select('\"' + feed.folder + '\"')
        connection.append('\"' + feed.folder + '\"', '', 
                            #imaplib.Time2Internaldate(parsed_date),
                            entry.time_published,
                            str.encode(str(msg), 'utf-8'))
        self.logger.debug('Stored entry "' + entry.title + '" at <' + 
                     self.username + '> in ' + feed.folder + '.')
        connection.close()
        return entry