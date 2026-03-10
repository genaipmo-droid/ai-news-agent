from tools import fetch_ai_news
from summarize import summarize_article, is_india_ai_related, score_news_impact
from email_sender import send_email
from llm_monitor import print_summary, log_to_file


def run_news_agent():

    articles = fetch_ai_news()

    scored_articles = []

    # Step 1 — Filter + Score
    for art in articles:

        title = art["title"]

        if not is_india_ai_related(title):
            continue

        score = score_news_impact(title)

        art["impact_score"] = score

        scored_articles.append(art)

    # Step 2 — Rank by impact
    scored_articles = sorted(
        scored_articles,
        key=lambda x: x["impact_score"],
        reverse=True
    )

    # Step 3 — Select top 5
    top_articles = scored_articles[:5]

    report = ""

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

    # Print token usage summary
    print_summary()

    # Save usage to CSV
    log_to_file()