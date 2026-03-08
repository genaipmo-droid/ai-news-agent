from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def is_ai_related(text):
    """
    Check if the news headline is related to AI.
    """

    prompt = f"""
Determine whether the following news headline is related to Artificial Intelligence.

Answer ONLY with YES or NO.

Headline:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    answer = response.choices[0].message.content.strip().upper()

    return answer == "YES"


def is_india_related(text):
    """
    Check if the news is specifically related to India.
    """

    prompt = f"""
Determine whether the following AI news headline is specifically related to India.

Answer ONLY with YES or NO.

Headline:
{text}
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
    Generate structured AI news summary.
    """

    prompt = f"""
You are writing a professional AI news briefing.

Return the summary EXACTLY in this structure.

Headline: One short sentence headline.

Bullets:
• point
• point
• point

Impact:
One sentence describing why this news matters.

News:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    output = response.choices[0].message.content

    # Format bullets for HTML email
    output = output.replace("•", "<br>• ")

    return output