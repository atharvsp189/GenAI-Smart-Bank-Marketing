import os
import yaml
import base64
from .Google import Create_Service
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from AgentManager.log import logger

base_dir = os.path.dirname(os.path.dirname(__file__))
credential_path = os.path.join(base_dir, "Email", "credentials.json")

class SendEmail:
    def __init__(self):
        self.CLIENT_SECRET_FILE = credential_path
        self.API_NAME = 'gmail'
        self.API_VERSION = 'v1'
        self.SCOPES = ['https://mail.google.com/']
        self.service = Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)
        logger.info("Email Service Initialized")

    def send_email_msg(self, userId='me', receiver: str = "apollonion72@gmail.com", subject: str = "Bank of Dholakpur", email_body="Get the best Experience with Bank of Dholakpur"):
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = receiver
        mimeMessage['subject'] = subject
        mimeMessage.attach(MIMEText(email_body, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        message = self.service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        logger.info(f"sending to {receiver}, message{message}")

