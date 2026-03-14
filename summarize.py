import os
import json
from openai import OpenAI
from llm_monitor import log_usage
from langsmith import traceable
import re


def parse_classifier_output(output):
    """
    Safely parse classifier JSON output and remove markdown code blocks.
    """
    try:
        cleaned = re.sub(r"```json|```", "", output).strip()
        data = json.loads(cleaned)
        return data.get("relevant", [])
    except Exception as e:
        print("Classifier JSON parsing failed:", e)
        return []


# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


def classify_india_ai_batch(headlines):
    """
    Classify multiple headlines in one LLM call.
    Returns a list of integer indices.
    """

    numbered_headlines = "\n".join(
        [f"{i}. {h}" for i, h in enumerate(headlines)]
    )

    prompt = f"""
You are a strict classifier.

Identify which headlines describe AI developments related to India.

Return ONLY raw JSON in this format:

{{ "relevant": [indices] }}

Example:
{{ "relevant": [0,2,5] }}

Do NOT include markdown or ``` blocks.

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

    print("Classifier raw output:", output)

    # ✅ Safe JSON parsing
    indices = parse_classifier_output(output)

    # Ensure indices are valid integers
    indices = [
        int(i) for i in indices
        if isinstance(i, int) or str(i).isdigit()
    ]

    return indices


@traceable
def score_news_impact(text):
    """
    Score importance of AI development in India (1–10).
    """

    prompt = f"""
Score the importance of this AI news headline related to India.

Return ONLY a number between 1 and 10.

Guidelines:

10 = Major national AI initiative or breakthrough
8-9 = Major company expansion or funding
6-7 = Significant startup or product launch
4-5 = Moderate development
1-3 = Minor update

Headline:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    log_usage(response.usage)

    output = response.choices[0].message.content.strip()

    try:
        return int(output)
    except:
        return 1


@traceable
def summarize_article(text):
    """
    Generate structured executive summary.
    """

    prompt = f"""
Write a short executive summary of this AI news headline related to India.

Use EXACT format:

Headline: one sentence summary

Key Points:
• bullet
• bullet
• bullet

Impact:
one sentence explaining significance for India's AI ecosystem.

Headline:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    log_usage(response.usage)

    output = response.choices[0].message.content

    # Convert bullet formatting for HTML email
    output = output.replace("•", "<br>• ")

    return output

@traceable
def classify_ai_category(text):
    """
    Categorize AI news related to India.
    """

    prompt = f"""
Classify this AI news headline into ONE category.

Categories:
1. Government AI Initiatives
2. AI Infrastructure Investments
3. Startup / Funding
4. Big Tech AI Developments
5. Research / Innovation

Return ONLY the category name.

Headline:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    log_usage(response.usage)

    return response.choices[0].message.content.strip()