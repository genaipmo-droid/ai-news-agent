from openai import OpenAI
import os

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
    Strict classifier: headline MUST BE BOTH AI-related AND India-related.
    """

    prompt = f"""
You are a strict classifier for Artificial Intelligence news related to India.

Your task is to determine whether the headline is about:
Artificial Intelligence developments specifically connected to India.

Return ONLY:

YES
or
NO

Return YES only if BOTH conditions are true:

1) The topic is about Artificial Intelligence, such as:
- AI
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

2) The news is specifically related to India, such as:
- Indian companies
- Indian startups
- Indian government
- Indian research labs
- Indian AI ecosystem
- Indian cities like Bengaluru, Delhi, Mumbai, Hyderabad, Chennai
- AI investments or infrastructure in India

Return NO if:
- It is about airlines, aviation, politics, finance, social issues
- It is global AI news not specifically about India
- It is India news unrelated to AI

Examples:

Headline: India launches national AI compute mission
Answer: YES

Headline: Nvidia expands AI research center in Bengaluru
Answer: YES

Headline: Indian startup builds generative AI platform
Answer: YES

Headline: OpenAI releases new GPT model
Answer: NO

Headline: Air India increases number of women pilots
Answer: NO

Headline:
{text}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    answer = response.choices[0].message.content.strip().upper()

    return answer == "YES"



def summarize_article(text):
    """
    Generate structured summary for the news headline.
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
- Impact must explain the significance for India's AI landscape.

News:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    output = response.choices[0].message.content

    # Make bullets render nicely in HTML emails
    output = output.replace("•", "<br>• ")

    return output