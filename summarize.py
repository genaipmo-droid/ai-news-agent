from openai import OpenAI
import os
from llm_monitor import log_usage

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is missing")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


def classify_india_ai_batch(headlines):
    """
    Classify multiple headlines in one LLM call.
    Returns a list of indices for relevant headlines.
    """

    numbered_headlines = "\n".join(
        [f"{i+1}. {h}" for i, h in enumerate(headlines)]
    )

    prompt = f"""
You are a strict news classifier.

From the list below, identify headlines describing
Artificial Intelligence developments specifically related to India.

Return ONLY the numbers of relevant headlines separated by commas.

Example output:
1,3,5

Rules:

Relevant headlines must:
1) Be about AI / machine learning / generative AI / LLMs
2) Be specifically related to India (Indian companies, startups,
government, research labs, or cities like Bengaluru, Delhi, etc.)

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

    try:
        indices = [int(x.strip()) - 1 for x in answer.split(",")]
        return indices
    except:
        return []


def score_news_impact(text):
    """
    Score importance of AI development in India.
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

Return ONLY a number between 1 and 10.

Headline:
{text}

Score:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )

    log_usage(response.usage, "Impact Scoring")

    score = response.choices[0].message.content.strip()

    try:
        return int(score)
    except:
        return 1



def summarize_article(text):
    """
    Generate structured executive summary.
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
- Bullet points must expand the headline.
- Impact must explain significance for India's AI ecosystem.

News:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )

    log_usage(response.usage, "Summarization")

    output = response.choices[0].message.content

    # HTML formatting for email
    output = output.replace("•", "<br>• ")

    return output