import logging
import threading
from secure_smtpd import SMTPServer, FakeCredentialValidator, LOG_NAME

class SSLSMTPServer(SMTPServer):
    def init(self):
        self._messages = []
    def process_message(self, peer, mailfrom, rcpttos, message_data):
        print(message_data)
        self._messages.append(message_data)
    def pop_messages(self):
        messages = self._messages
        self._messages = []
        return messages
    def start(self):
        self._thread = threading.Thread(target=self.run)
        self._thread.start()
    def stop(self):
        self._thread.join()

if __name__ == '__main__':
    logger = logging.getLogger( LOG_NAME )
    logger.setLevel(logging.INFO)

    server = SSLSMTPServer(
        ('0.0.0.0', 1025),
        None,
        require_authentication=True,
        ssl=True,
        certfile='server.crt',
        keyfile='server.key',
        credential_validator=FakeCredentialValidator(),
        maximum_execution_time = 1.0
        )

    server.run()
