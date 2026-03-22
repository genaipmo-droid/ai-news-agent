from crew_runner import run_news_agent

from langsmith import traceable

@traceable(name="AI News Agent Run")
def main():
    run_news_agent()

if __name__ == "__main__":
    main()
