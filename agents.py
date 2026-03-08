from crewai import Agent


research_agent = Agent(
    role="AI News Researcher",
    goal="Find the latest AI developments in India",
    backstory="Technology journalist tracking AI innovation in India.",
    verbose=True
)


relevance_agent = Agent(
    role="Relevance Analyst",
    goal="Determine if a news article is related to India",
    backstory="Expert in analyzing AI developments in India.",
    verbose=True
)


summarizer_agent = Agent(
    role="AI News Summarizer",
    goal="Create concise AI news summaries",
    backstory="Writes executive briefings for technology leaders.",
    verbose=True
)


editor_agent = Agent(
    role="Chief Editor",
    goal="Select the most important AI developments",
    backstory="Responsible for daily AI intelligence reports.",
    verbose=True
)