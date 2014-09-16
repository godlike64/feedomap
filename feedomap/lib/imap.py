import imaplib
import time
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from feedomap.lib.utils import striphtml, craft_message

class IMAPConnection(object):
    
    def __init__(self, host, username, password, port):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
    
    def connect(self):
        self.connection = imaplib.IMAP4(host=self.host, port=self.port)
        if self.port == 143:
            self.connection.starttls()
        self.connection.login(self.username, self.password)
    
    def store_entry(self, feed, entry):
        parsed_date = time.mktime(entry.published_parsed)
        msg = craft_message(self.username, feed, entry)
        
        self.connection.append('INBOX', '', 
                               #imaplib.Time2Internaldate(parsed_date),
                               parsed_date,
                               str.encode(str(msg), 'utf-8'))
