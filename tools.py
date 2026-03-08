import feedparser
from datetime import datetime


def fetch_ai_news():

    url = "https://news.google.com/rss/search?q=AI+India&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries:

        date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")

        articles.append({
            "title": entry.title,
            "link": entry.link,
            "publisher": entry.source.title,
            "date": date
        })

    return articles