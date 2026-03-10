import datetime

# Global counters
TOTAL_PROMPT_TOKENS = 0
TOTAL_COMPLETION_TOKENS = 0
TOTAL_TOKENS = 0

# Pricing for gpt-4o-mini (approx)
INPUT_COST_PER_1K = 0.00015
OUTPUT_COST_PER_1K = 0.00060


def log_usage(usage, label=None):
    """
    Track token usage silently without printing per-call logs.
    """

    global TOTAL_PROMPT_TOKENS
    global TOTAL_COMPLETION_TOKENS
    global TOTAL_TOKENS

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    total_tokens = usage.total_tokens

    TOTAL_PROMPT_TOKENS += prompt_tokens
    TOTAL_COMPLETION_TOKENS += completion_tokens
    TOTAL_TOKENS += total_tokens


def print_summary():
    """
    Print final usage summary only.
    """

    input_cost = (TOTAL_PROMPT_TOKENS / 1000) * INPUT_COST_PER_1K
    output_cost = (TOTAL_COMPLETION_TOKENS / 1000) * OUTPUT_COST_PER_1K
    total_cost = input_cost + output_cost

    print("\n===============================")
    print("LLM USAGE SUMMARY")
    print("===============================")
    print("Prompt tokens:", TOTAL_PROMPT_TOKENS)
    print("Completion tokens:", TOTAL_COMPLETION_TOKENS)
    print("Total tokens:", TOTAL_TOKENS)
    print("Estimated cost: $", round(total_cost, 6))
    print("===============================\n")


def log_to_file():
    """
    Save usage to CSV log.
    """

    date = datetime.date.today()

    with open("token_usage_log.csv", "a") as f:
        f.write(f"{date},{TOTAL_TOKENS}\n")