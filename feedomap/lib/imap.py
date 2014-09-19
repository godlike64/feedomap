import imaplib
import time
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from feedomap.lib.utils import striphtml, craft_message

class IMAPConnection(object):
    
    def __init__(self, host, port, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
    
    def connect(self):
        if self.port == 993:
            self.connection = imaplib.IMAP4_SSL(host=self.host, port=self.port)
        else:
            self.connection = imaplib.IMAP4(host=self.host, port=self.port)
            if self.port == 143:
                self.connection.starttls()
        self.connection.login(self.username, self.password)
    
    def store_entry(self, feed, entry, folder):
        parsed_date = time.mktime(entry.published_parsed)
        msg = craft_message(self.username, feed.contents['feed'], entry, 
                            feed.sender)
        self.connection.create(folder)
        self.connection.append(folder, '', 
                               #imaplib.Time2Internaldate(parsed_date),
                               parsed_date,
                               str.encode(str(msg), 'utf-8'))
