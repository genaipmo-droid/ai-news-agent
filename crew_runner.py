
from dotenv import load_dotenv
import os

load_dotenv()

from tools import fetch_ai_news
from summarize import summarize_article, is_india_ai_related
from email_sender import send_email


def run_news_agent():

    articles = fetch_ai_news()

    report = ""
    count = 0

    # Optional cheap keyword filter before LLM
    ai_keywords = [
        "ai",
        "artificial intelligence",
        "machine learning",
        "generative ai",
        "deep learning",
        "llm",
        "neural",
        "nvidia",
        "openai"
    ]

    for art in articles:

        title = art["title"]

        # Keyword filter to reduce noise
        if not any(k in title.lower() for k in ai_keywords):
            continue

        # LLM judge for India + AI relevance
        if not is_india_ai_related(title):
            continue

        # Summarize the news
        summary = summarize_article(title)

        # Format sections nicely for HTML email
        summary = summary.replace("Headline:", "<b>Headline:</b><br>")
        summary = summary.replace("Key Points:", "<br><b>Key Points:</b>")
        summary = summary.replace("Impact:", "<br><b>Impact:</b><br>")

        report += "<br>----------------------<br><br>"
        report += f"<b>{art['date']}</b><br><br>"
        report += summary
        report += f'<br><br>Source: <a href="{art["link"]}">{art["publisher"]}</a>'
        report += "<br><br>"

        count += 1

        # Stop after top 5 news
        if count == 5:
            break

    if count == 0:
        report = "No India-specific AI news found today."

    send_email(report)

    print("Daily AI News Email Sent Successfully")