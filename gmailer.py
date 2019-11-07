import logging
import smtplib
import json

from email import encoders
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def _load_gmail_settings(settings_file_name):
    with open(settings_file_name, 'r') as f:
        settings = f.read()
    return json.loads(settings)

class Gmailer:
    def __init__(self, settings_file_name):
        gmail_settings = _load_gmail_settings(settings_file_name)
        self._gmail_account = gmail_settings['GMAIL_ADDRESS']
        self._gmail_password = gmail_settings['GMAIL_PASSWORD']

    def _send_gmail(self, to_address, msg):
        logging.info('Sending email from %s to %s' % (self._gmail_account, to_address))
        try:
            logging.info('Connecting to gmail SMTP server')
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            logging.info('Logging into gmail SMTP server as %s' % self._gmail_account)
            server.login(self._gmail_account, self._gmail_password)
            logging.info('Sending email to %s' % to_address)
            server.sendmail(self._gmail_account, to_address, msg.as_string())    
            logging.info('Closing connection to gmail SMTP server')
            server.close()
            return True
        except Exception as e:
            logging.error('Exception sending email: %s' % str(e))
            return False

    def send_gmail(self, to_address, subject, message):
        try:
            msg = MIMEText(message)
            msg['From'] = '"Raspberry Pi Security Camera" <%s>' % self._gmail_account
            msg['To'] = to_address
            msg['Subject'] = subject
            return self._send_gmail(to_address, msg)
        except Exception as e:
            logging.error('Exception sending email: %s' % str(e))
            return False

    def send_gmail_with_attached_file(self, to_address, subject, message, file_name):
        try:
            msg = MIMEMultipart(message)
            msg['From'] = '"Raspberry Pi Security Camera" <%s>' % self._gmail_account
            msg['To'] = to_address
            msg['Subject'] = subject
            with open(file_name, 'rb') as fd:
                img = MIMEBase('video', 'x-matroska')
                img.set_payload(fd.read())
                encoders.encode_base64(img)
                img.add_header('Content-Disposition', 'attachment', filename=os.path.split(file_name)[-1])
                msg.attach(img)
            return self._send_gmail(to_address, msg)
        except Exception as e:
            logging.error('Exception sending email with attachment %s: %s' % (file_name, str(e)))
            return False
