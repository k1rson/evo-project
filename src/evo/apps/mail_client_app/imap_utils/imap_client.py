import imaplib

from django.conf import settings

class IMAPServer: 
    def __init__(self):
        self.connection_open = False
        self.imap_connection = self._open_connection()

    def _open_connection(self) -> bool:
        if not self.connection_open:
            try: 
                self.imap_connection = imaplib.IMAP4_SSL(settings.IMAP_SERVER, settings.IMAP_PORT, timeout=3)
                self.imap_connection.login(settings.IMAP_USERNAME, settings.IMAP_PASSWORD)
            except: 
                return False

            self.connection_open = True
            return True
        else: 
            return False

    def close_connection(self) -> bool:
        if self.connection_open:
            self.imap_connection.close()
            self.connection_open = False

    def get_all_messages(self) -> list:
        pass

    def get_unread_messages(self) -> list:
        pass

    def get_read_messages(self) -> list:
        pass

    