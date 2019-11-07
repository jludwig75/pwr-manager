from datetime import datetime
from gmailer import Gmailer

class EmailWatcher:
    def __init__(self, gmail_settings_file_name, notification_address):
        self._mailer = Gmailer(gmail_settings_file_name)
        self._notification_address = notification_address
    def notify_event(self, event_message):
        self._mailer.send_gmail(self._notification_address,
                                subject=event_message,
                                message='Plug power change event at %s: %s' % (str(datetime.now()), event_message))
