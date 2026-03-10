from tools import fetch_ai_news
from summarize import (
    classify_india_ai_batch,
    summarize_article,
    score_news_impact
)
from email_sender import send_email
from llm_monitor import print_summary, log_to_file


def run_news_agent():

    print("Starting AI News Agent...")

    articles = fetch_ai_news()

    if not articles:
        print("No articles fetched")
        return

    # Extract titles
    titles = [a["title"] for a in articles]

    # Step 1 — Batch classification
    relevant_indices = classify_india_ai_batch(titles)

    relevant_articles = [articles[i] for i in relevant_indices]

    scored_articles = []

    # Step 2 — Impact scoring
    for art in relevant_articles:

        score = score_news_impact(art["title"])
        art["impact_score"] = score

        scored_articles.append(art)

    # Step 3 — Rank by importance
    scored_articles = sorted(
        scored_articles,
        key=lambda x: x["impact_score"],
        reverse=True
    )

    top_articles = scored_articles[:5]

    report = ""

    # Step 4 — Summarize
    for art in top_articles:

        summary = summarize_article(art["title"])

        summary = summary.replace("Headline:", "<b>Headline:</b><br>")
        summary = summary.replace("Key Points:", "<br><b>Key Points:</b>")
        summary = summary.replace("Impact:", "<br><b>Impact:</b><br>")

        report += "<br>----------------------<br><br>"
        report += f"<b>{art['date']}</b> | Impact Score: {art['impact_score']}<br><br>"
        report += summary
        report += f'<br><br>Source: <a href="{art["link"]}">{art["publisher"]}</a>'
        report += "<br><br>"

    if not report:
        report = "No AI developments related to India were found today."

    send_email(report)

    print("Top AI News Email Sent Successfully")

    print_summary()
    log_to_file()