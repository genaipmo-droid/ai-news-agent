import smtplib
from email.mime.text import MIMEText
import os


def send_email(content):

    msg = MIMEText(content, "html")

    msg["Subject"] = "Daily AI News Digest - India"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_TO")

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:

        server.login(
            os.getenv("EMAIL_USER"),
            os.getenv("EMAIL_PASS")
        )

        server.send_message(msg)