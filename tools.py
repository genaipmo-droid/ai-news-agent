import feedparser
from datetime import datetime


def fetch_ai_news():

    rss_url = "https://news.google.com/rss/search?q=artificial+intelligence+India&hl=en-IN&gl=IN&ceid=IN:en"

    print("Fetching RSS:", rss_url)

    feed = feedparser.parse(rss_url)

    print("RSS entries found:", len(feed.entries))

    articles = []

    for entry in feed.entries:

        try:
            title = entry.title
            link = entry.link

            published = entry.published if "published" in entry else ""

            publisher = entry.source.title if "source" in entry else "Unknown"

            articles.append({
                "title": title,
                "link": link,
                "publisher": publisher,
                "date": published
            })

        except Exception as e:
            print("Error parsing entry:", e)

    print("Articles parsed:", len(articles))

    return articles