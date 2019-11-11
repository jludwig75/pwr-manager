from datetime import datetime
from mailer import Mailer
import logging

class EmailWatcher:
    def __init__(self, mail_settings_file_name, notification_address):
        self._mailer = Mailer(mail_settings_file_name, 'KASA SmartPlug Power Manager')
        self._notification_address = notification_address
        logging.info('Email notifications will be sent to %s' % self._notification_address)
    def notify_event(self, event_message):
        self._mailer.send_mail(self._notification_address,
                                subject=event_message,
                                message='SmartPlug power event at %s: %s' % (str(datetime.now()), event_message))
