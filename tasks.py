from crewai import Task
from agents import research_agent, relevance_agent, summarizer_agent, editor_agent


research_task = Task(
    description="Collect AI news related to India",
    agent=research_agent,
    expected_output="List of AI news articles"
)


relevance_task = Task(
    description="Check if the news article is related to India",
    agent=relevance_agent,
    expected_output="YES or NO"
)


summary_task = Task(
    description="Summarize AI news",
    agent=summarizer_agent,
    expected_output="Headline, bullet points, impact statement"
)


editor_task = Task(
    description="Select top 5 AI developments",
    agent=editor_agent,
    expected_output="Top 5 AI news"
)