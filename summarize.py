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

    numbered_headlines = "\n".join(
        [f"{i+1}. {h}" for i, h in enumerate(headlines)]
    )

    prompt = f"""
You are a strict news classifier.

From the list below, identify headlines describing
Artificial Intelligence developments specifically related to India.

Return ONLY the numbers of relevant headlines separated by commas.

Example:
1,3,5

Headlines:

{numbered_headlines}

Relevant headline numbers:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    log_usage(response.usage)

    answer = response.choices[0].message.content.strip()

    # Convert LLM output to integer indices
    try:
        numbers = answer.replace(" ", "").split(",")
        indices = [int(n) - 1 for n in numbers if n.isdigit()]
        return indices
    except Exception:
        return []


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