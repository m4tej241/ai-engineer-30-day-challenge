"""
Day 2 — reference solution. Try exercise.py yourself first.
"""

import os
import time
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise SystemExit(
        "ANTHROPIC_API_KEY not set. Make sure .env exists in the project root "
        "with your key from console.anthropic.com/settings/keys"
    )

client = Anthropic(api_key=api_key)
MODEL = "claude-sonnet-4-5-20250929"


def exercise_1_basic_stream():
    print("\n--- Exercise 1: basic streaming ---")
    prompt = "Explain what a REST API is, in 3 sentences."
    with client.messages.stream(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print()  # newline after streaming finishes


def exercise_2_collect_full_text():
    print("\n--- Exercise 2: collecting the streamed text ---")
    prompt = "List 3 benefits of streaming API responses."
    full_text = ""
    with client.messages.stream(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_text += text
    print("\n\nReconstructed full text:")
    print(full_text)


def exercise_3_usage_after_stream():
    print("\n--- Exercise 3: usage after stream ends ---")
    prompt = "Say hello in three languages."
    with client.messages.stream(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

        # Calling get_final_message() here, before the loop above has fully
        # drained, forces the SDK to block and finish consuming the stream
        # first -- it does NOT error, but it defeats the point of streaming
        # since you're now waiting synchronously. Uncomment to see:
        # early_final = stream.get_final_message()
        # print("\n(fetched final message before loop technically 'ended')")

    # Correct place: after the with-block, the stream is fully closed.
    final_message = stream.get_final_message()
    print(f"\ninput_tokens={final_message.usage.input_tokens}, "
          f"output_tokens={final_message.usage.output_tokens}")


def exercise_4_time_to_first_token():
    print("\n--- Exercise 4: time to first token ---")
    prompt = "Explain the difference between synchronous and asynchronous code, in detail."

    # Streaming
    start = time.perf_counter()
    first_token_time = None
    with client.messages.stream(
        model=MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            if first_token_time is None:
                first_token_time = time.perf_counter()
            # not printing the text here to keep the timing output readable
    stream_end = time.perf_counter()
    print(f"[streaming] first token after: {first_token_time - start:.3f}s")
    print(f"[streaming] total: {stream_end - start:.3f}s")

    # Non-streaming
    start = time.perf_counter()
    client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    end = time.perf_counter()
    print(f"[non-streaming] total: {end - start:.3f}s (no meaningful 'first token' time)")


if __name__ == "__main__":
    exercise_1_basic_stream()
    exercise_2_collect_full_text()
    exercise_3_usage_after_stream()
    exercise_4_time_to_first_token()
