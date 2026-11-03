"""
Day 1 — LLM APIs: talking to Claude directly in Python.

Work through the TODOs in order. Run this file after each one:
    python exercise.py

See day-01/README.md for the concepts and exercise descriptions.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise SystemExit(
        "ANTHROPIC_API_KEY not set. Copy day-01/.env.example to .env in the "
        "project root and paste your key from console.anthropic.com/settings/keys"
    )

client = Anthropic(api_key=api_key)

# Model name is a versioned string. If this errors as "model not found",
# check https://console.anthropic.com/docs for the current list.
MODEL = "claude-haiku-4-5-20251001"


def exercise_1_basic_call():
    """TODO 1: Send a single user message and print the response text."""
    print("\n--- Exercise 1: basic call ---")
    # TODO: call client.messages.create(...) with:
    #   model=MODEL
    #   max_tokens=200
    #   messages=[{"role": "user", "content": "Explain what an API is, in 2 sentences."}]
    # Then print response.content[0].text
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": "Explain what an API is, in 2 sentences."}],
    )
    print(response.content[0].text)


def exercise_2_system_prompt():
    """TODO 2: Same call, but add a system prompt and compare."""
    print("\n--- Exercise 2: with system prompt ---")
    # TODO: same call as exercise 1, but add:
    #   system="You are a terse, no-nonsense senior engineer. Answer in one sentence."
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": "Explain what an API is, in 2 sentences."}],
        system="You are a terse, no-nonsense senior engineer. Answer in one sentence.",
    )
    print(response.content[0].text)


def exercise_3_temperature_comparison():
    """TODO 3: Same prompt at temperature=0 vs temperature=1. Run this function 2-3 times."""
    print("\n--- Exercise 3: temperature comparison ---")
    prompt = "Give me one interesting fact about the ocean."
    # TODO: call the same prompt twice, once with temperature=0, once with temperature=1
    # Print both outputs labeled clearly (e.g. "temp=0:" / "temp=1:")
    response_temp0 = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    response_temp1 = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
    )
    print(response_temp0.content[0].text)
    print(response_temp1.content[0].text)


def exercise_4_token_usage():
    """TODO 4: Print token usage for a call."""
    print("\n--- Exercise 4: token usage ---")
    # TODO: make any call, then print:
    #   response.usage.input_tokens
    #   response.usage.output_tokens
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": "What is the weather today in New York?"}],
    )
    print(response.usage.input_tokens)
    print(response.usage.output_tokens)


def exercise_5_stretch():
    prompt = input()
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    print(response.content[0].text)

if __name__ == "__main__":
    # exercise_1_basic_call()
    exercise_2_system_prompt()
    exercise_3_temperature_comparison()
    exercise_4_token_usage()
