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


def is_india_ai_related(text):
    """
    Contextual classifier to determine if headline is AI-related AND India-related.
    """

    prompt = f"""
You are a strict news classifier.

Determine whether the headline describes a development in
Artificial Intelligence specifically related to India.

Return ONLY:

YES
or
NO

Return YES only if BOTH conditions are true:

1) The topic clearly relates to Artificial Intelligence such as:
- artificial intelligence
- machine learning
- deep learning
- generative AI
- LLMs
- AI research
- AI startups
- AI policy
- AI infrastructure
- AI models
- AI tools

AND

2) The development is specifically connected to India such as:
- Indian companies
- Indian startups
- Indian government
- Indian research labs
- Indian AI ecosystem
- Indian cities like Bengaluru, Delhi, Mumbai, Hyderabad, Chennai

Return NO if:
- The headline is about airlines, aviation, politics, finance, etc.
- The topic is global AI news not specifically about India
- The topic is India news unrelated to AI

Headline:
{text}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    log_usage(response.usage, "AI + India Classifier")

    answer = response.choices[0].message.content.strip().upper()

    return answer == "YES"



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