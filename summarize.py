import os
import json
from openai import OpenAI
from llm_monitor import log_usage
from langsmith import traceable


# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


@traceable
def classify_india_ai_batch(headlines):
    """
    Classify multiple headlines in one LLM call.
    Returns list of indices of relevant headlines.
    """

    numbered_headlines = "\n".join(
        [f"{i}. {h}" for i, h in enumerate(headlines)]
    )

    prompt = f"""
You are a strict news classifier.

Identify headlines describing Artificial Intelligence developments
specifically related to India.

Return the result in JSON format ONLY:

{{
  "relevant": [indices]
}}

Example:
{{
  "relevant": [0,2,5]
}}

Rules:
1. The news must clearly relate to AI / machine learning / generative AI / LLMs
2. The development must specifically involve India
3. Return only JSON, no explanations

Headlines:

{numbered_headlines}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    log_usage(response.usage)

    output = response.choices[0].message.content.strip()

    try:
        data = json.loads(output)
        return data.get("relevant", [])
    except Exception:
        return []


@traceable
def score_news_impact(text):
    """
    Score importance of AI development in India (1–10).
    """

    prompt = f"""
You are evaluating the importance of an AI development related to India.

Score the impact from 1 to 10.

Score guide:

10 = Major national AI policy, infrastructure, or breakthrough
8-9 = Large investments, major AI company expansion, major research
6-7 = Significant AI startup launches or partnerships
4-5 = Moderate AI developments
1-3 = Minor updates

Return ONLY the number.

Headline:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )

    log_usage(response.usage)

    try:
        return int(response.choices[0].message.content.strip())
    except:
        return 1


@traceable
def summarize_article(text):
    """
    Generate structured executive summary for AI news.
    """

    prompt = f"""
You are writing an executive briefing on AI developments in India.

Summarize the news using EXACTLY this structure:

Headline: One clear sentence summarizing the news.

Key Points:
• bullet point
• bullet point
• bullet point

Impact:
One sentence explaining why this development matters for India's AI ecosystem.

Rules:
- Headline must be ONE sentence.
- Exactly 3 bullet points.
- Each bullet must start with "•".
- Impact must explain significance for India's AI ecosystem.

News:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )

    log_usage(response.usage)

    output = response.choices[0].message.content

    # Improve formatting for HTML email
    output = output.replace("•", "<br>• ")

    return output