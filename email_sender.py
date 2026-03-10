import smtplib
import os
from email.mime.text import MIMEText


def send_email(content):

    msg = MIMEText(content, "html")

    msg["Subject"] = "AI Developments in India – Daily Brief"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_TO")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(
        os.getenv("EMAIL_USER"),
        os.getenv("EMAIL_PASS")
    )

    server.sendmail(
        os.getenv("EMAIL_USER"),
        os.getenv("EMAIL_TO"),
        msg.as_string()
    )

    server.quit()