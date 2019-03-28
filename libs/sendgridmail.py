from sendgrid import SendGridAPIClient
import os
from sendgrid.helpers.mail import Email, Content, Mail
from libs.strings import gettext


class SendGridException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SendGridMail:
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    FROM_EMAIL = Email("info@rooms-escape.com")
    SUBJECT = "Welcome to Escape Rooms"

    @classmethod
    def send_email(cls, email: str, text: str,):
        if cls.SENDGRID_API_KEY is None:
            raise SendGridException(gettext("mailgun_failed_load_api_key"))

        sg = SendGridAPIClient(apikey=cls.SENDGRID_API_KEY)

        mail = Mail(cls.FROM_EMAIL, cls.SUBJECT, Email(email), Content("text/plain", text))

        response = sg.client.mail.send.post(request_body=mail.get())

        if response.status_code != 202:
            raise SendGridException(gettext("mailgun_error_send_email"))

        return response

