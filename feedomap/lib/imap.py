import imaplib

class IMAPConnection(object):
    
    def __init__(self, server, username, password, port):
        self.server = server
        self.username = username
        self.password = password
        self.port = port