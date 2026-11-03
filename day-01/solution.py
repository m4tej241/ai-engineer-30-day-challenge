"""
Day 1 — reference solution. Try exercise.py yourself first.
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
MODEL = "claude-sonnet-4-5-20250929"


def exercise_1_basic_call():
    print("\n--- Exercise 1: basic call ---")
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": "Explain what an API is, in 2 sentences."}],
    )
    print(response.content[0].text)


def exercise_2_system_prompt():
    print("\n--- Exercise 2: with system prompt ---")
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system="You are a terse, no-nonsense senior engineer. Answer in one sentence.",
        messages=[{"role": "user", "content": "Explain what an API is, in 2 sentences."}],
    )
    print(response.content[0].text)


def exercise_3_temperature_comparison():
    print("\n--- Exercise 3: temperature comparison ---")
    prompt = "Give me one interesting fact about the ocean."

    response_t0 = client.messages.create(
        model=MODEL,
        max_tokens=150,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    print("temp=0:", response_t0.content[0].text)

    response_t1 = client.messages.create(
        model=MODEL,
        max_tokens=150,
        temperature=1,
        messages=[{"role": "user", "content": prompt}],
    )
    print("temp=1:", response_t1.content[0].text)


def exercise_4_token_usage():
    print("\n--- Exercise 4: token usage ---")
    response = client.messages.create(
        model=MODEL,
        max_tokens=100,
        messages=[{"role": "user", "content": "Say hello in five languages."}],
    )
    print(response.content[0].text)
    print(f"input_tokens={response.usage.input_tokens}, output_tokens={response.usage.output_tokens}")


if __name__ == "__main__":
    exercise_1_basic_call()
    exercise_2_system_prompt()
    exercise_3_temperature_comparison()
    exercise_4_token_usage()
