from openai import OpenAI
import os
from llm_monitor import log_usage
from langsmith import traceable

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


@traceable
def classify_india_ai_batch(headlines):

    prompt = f"..."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    log_usage(response.usage)

    return response.choices[0].message.content.strip()


@traceable
def score_news_impact(text):

    prompt = f"..."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )

    log_usage(response.usage)

    return int(response.choices[0].message.content.strip())


@traceable
def summarize_article(text):

    prompt = f"..."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )

    log_usage(response.usage)

    return response.choices[0].message.content