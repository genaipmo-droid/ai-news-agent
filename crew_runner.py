from tools import fetch_ai_news
from summarize import summarize_article, is_india_ai_related
from email_sender import send_email


def run_news_agent():

    articles = fetch_ai_news()

    report = ""
    count = 0

    for art in articles:

        title = art["title"]

        # Contextual AI + India relevance filter
        if not is_india_ai_related(title):
            continue

        # Generate summary
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

        if count == 5:
            break

    if count == 0:
        report = "No AI developments related to India were found today."

    send_email(report)

    print("Daily AI News Email Sent Successfully")