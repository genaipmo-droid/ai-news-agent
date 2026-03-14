import feedparser
from datetime import datetime, timedelta, timezone


def fetch_ai_news():

    url = "https://news.google.com/rss/search?q=artificial+intelligence+India&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)

    articles = []

    now = datetime.now(timezone.utc)
    seven_days_ago = now - timedelta(days=7)

    for entry in feed.entries:

        try:
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        except:
            continue

        # Keep only last 7 days news
        if published < seven_days_ago:
            continue

        articles.append({

            "title": entry.title,
            "link": entry.link,
            "publisher": entry.source.title if "source" in entry else "Unknown",
            "date": published.strftime("%d %b %Y")

        })

    print("Articles parsed:", len(articles))

    return articles