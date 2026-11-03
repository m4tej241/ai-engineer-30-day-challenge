"""
Day 2 — Streaming responses.

Work through the TODOs in order. Run this file after each one:
    python exercise.py

See day-02/README.md for the concepts and exercise descriptions.
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
MODEL = "claude-haiku-4-5-20251001"


def exercise_1_basic_stream():
    """TODO 1: Stream a response and print each chunk as it arrives."""
    print("\n--- Exercise 1: basic streaming ---")
    prompt = "Explain what a REST API is, in 3 sentences."
    # TODO: open `with client.messages.stream(model=MODEL, max_tokens=300,
    #   messages=[{"role": "user", "content": prompt}]) as stream:`
    # then `for text in stream.text_stream: print(text, end="", flush=True)`
    
    with client.messages.stream(model=MODEL, max_tokens=300, messages=[{"role": "user", "content": prompt}]) as stream:
        for text in stream.text_stream:
            print(text)
        final_message = stream.get_final_message()


def exercise_2_collect_full_text():
    """TODO 2: Stream, print progressively, AND build up the full string."""
    print("\n--- Exercise 2: collecting the streamed text ---")
    prompt = "List 3 benefits of streaming API responses."
    # TODO: same streaming loop as exercise 1, but append each chunk to a
    # `full_text = ""` string as you go. After the `with` block, print
    # full_text again to show you reconstructed the complete response.
   
    with client.messages.stream(model=MODEL, max_tokens=300, messages=[{"role": "user", "content": prompt}]) as stream:
        full_text = ""
        for text in stream.text_stream:
            full_text += text
    print(full_text)


def exercise_3_usage_after_stream():
    """TODO 3: Read usage after the stream closes — and see what breaks if you don't wait."""
    print("\n--- Exercise 3: usage after stream ends ---")
    prompt = "Say hello in three languages."
    # TODO: run the streaming loop inside `with client.messages.stream(...) as stream:`,
    # then AFTER the with-block exits, call `stream.get_final_message()` and print
    # its `.usage.input_tokens` / `.usage.output_tokens`.
    #
    # Then, separately, try calling `stream.get_final_message()` *inside* the
    # with-block before the text_stream loop has finished iterating, and see
    # what happens (comment this part back out once you've seen the result).

    with client.messages.stream(model=MODEL, max_tokens= 300, messages=[{"role": "user", "content": prompt}]) as stream:
        for text in stream.text_stream:
            print(text)
        final_message = stream.get_final_message()
    print(final_message)


def exercise_4_time_to_first_token():
    """TODO 4: Compare time-to-first-token for streaming vs. non-streaming."""
    print("\n--- Exercise 4: time to first token ---")
    prompt = "Explain the difference between synchronous and asynchronous code, in detail."

    # TODO (streaming): record time.perf_counter() before opening the stream.
    # Inside the text_stream loop, on the FIRST chunk only, record a second
    # timestamp and print "first token after: X s". After the loop ends,
    # record a third timestamp and print "stream total: Y s".

    # TODO (non-streaming): record time.perf_counter() before calling
    # client.messages.create(...) with the same prompt, and again right after
    # it returns. Print "non-streaming total: Z s" — note there's no
    # meaningful "first token" time here, since the whole response arrives at once.
    
    s1 = time.perf_counter()
    f1 = True
    with client.messages.stream(model=MODEL, max_tokens=300, messages=[{"role":"user", "content": prompt}]) as stream:
        for text in stream.text_stream:
            if f1:
                print("first token after: ", time.perf_counter()," s")
                f1 = False
    s3 = time.perf_counter()
    print("stream total: ", s3 - s1, "s")

    s4 = time.perf_counter()
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    s5 = time.perf_counter()
    print("non-streaming total: ", s5 - s4, "s")


if __name__ == "__main__":
    exercise_1_basic_stream()
    exercise_2_collect_full_text()
    exercise_3_usage_after_stream()
    exercise_4_time_to_first_token()
