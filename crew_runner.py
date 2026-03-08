
from dotenv import load_dotenv
import os

load_dotenv()

from tools import fetch_ai_news
from summarize import summarize_article, is_india_related
from email_sender import send_email


def run_news_agent():

    articles = fetch_ai_news()

    report = ""
    count = 0

    for art in articles:

        if not is_india_related(art["title"]):
            continue

        summary = summarize_article(art["title"])
        
      # Format sections nicely for email
        summary = summary.replace("Headline:", "<b>Headline:</b><br>")
        summary = summary.replace("Bullets:", "<br><b>Key Points:</b>")
        summary = summary.replace("Impact:", "<br><b>Impact:</b><br>")

        report += "<br>----------------------<br><br>"
        report += f"<b>{art['date']}</b><br><br>"
        report += summary
        report += f'<br><br>Source: <a href="{art["link"]}">{art["publisher"]}</a>'
        report += "<br><br>"

        count += 1

        if count == 5:
            break

    send_email(report)

    print("Daily AI News Email Sent")