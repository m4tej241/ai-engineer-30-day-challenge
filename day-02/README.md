# Day 2 — Streaming responses

**Time budget:** ~1.5 hours
**Prereqs:** Day 1 done, `.venv` active, `ANTHROPIC_API_KEY` in the project-root `.env`

## Why this matters

Yesterday every call blocked until the whole response was ready. Fine for a 2-sentence answer — but stretch that to a multi-paragraph explanation and the user stares at a spinner for several seconds before anything shows up. Streaming is why Claude.ai/ChatGPT feel instant: the server sends the response token-by-token as it's generated, and the client renders each piece as it arrives. Perceived latency becomes "time to first token," not "time to full answer."

**Analogy:** a normal API call is a Custom Connector's synchronous action — you wait for the whole HTTP response body. Streaming is closer to a long-running Power Automate flow where you'd normally poll a queue for partial progress — except here the server pushes updates to you over one held-open connection instead of you polling it.

## Core concept: what a streamed response actually is

Under the hood, the API upgrades the response into a stream of small JSON events (Server-Sent Events):

- `message_start` — stream opened, empty message shell
- `content_block_start` — a content block begins (e.g. text)
- `content_block_delta` — the payload, arriving many times; each one is a `text_delta` carrying a small piece of text
- `content_block_stop` — that block is finished
- `message_delta` — carries the final `stop_reason` and token usage once generation is done
- `message_stop` — stream closed

You *could* handle these raw events yourself, but the Python SDK wraps the plumbing in a context manager:

```python
with client.messages.stream(model=MODEL, max_tokens=500, messages=[...]) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final_message = stream.get_final_message()  # full Message object — same shape as Day 1, usage included
```

`stream.text_stream` gives you just the text deltas, already assembled in order — that's what you'll use almost all the time. `get_final_message()` is available once the `with` block exits, for anything you'd normally read off a non-streaming response (`usage`, `stop_reason`, etc.) — trying to read it mid-stream is a common mistake, see exercise 3.

## Exercises

Open `exercise.py`. It has 4 `TODO` sections — do them in order, run the script after each one.

1. **Basic stream.** Send one user message and print the response as it arrives, chunk by chunk, using `stream.text_stream`. Watch it print progressively instead of all at once.
2. **Collect the full text.** Same call, but also accumulate the streamed chunks into one string as you print them, and print the assembled string again at the end. (This is what you'd store if you were saving the reply to a database or a conversation log.)
3. **Usage after the stream ends.** Use `stream.get_final_message()` *after* the `with` block exits and print `usage.input_tokens` / `usage.output_tokens`. Then, just to see the failure mode, try printing `stream.get_final_message()` *inside* the `with` block, before the loop finishes — what happens?
4. **Time to first token vs. total time.** For the *same* prompt, time a streaming call (record the timestamp when the first chunk arrives, and when the stream closes) and a non-streaming call (`client.messages.create`, one timestamp before, one after). Print both: "time to first token" and "total time" for each approach.

## Stretch goal (optional)

Turn exercise 1 into a tiny "typing effect" CLI: `input()` a prompt, stream the answer to the terminal as it's generated. Still single-turn, no memory — that's still Day 3. The point here is purely the UX difference of watching it type versus waiting for a wall of text.

## Reflection questions

- Why is "time to first token" a more meaningful UX metric than total response time, especially for longer answers?
- What actually broke when you tried to read `get_final_message()` before the stream finished? What does that tell you about what the SDK has and hasn't received yet at that point?
- If you were wrapping this as a Custom Connector for Copilot Studio, would streaming even survive the trip to the end user — or does Copilot Studio's own response model flatten it back into a single blocking reply? Worth checking next time you're in there.

## Done when

- [ ] All 4 TODOs in `exercise.py` run without errors
- [ ] You can explain in your own words: what a `text_delta` is, why `get_final_message()` only works after the stream closes, and why time-to-first-token matters
- [ ] You've answered the 3 reflection questions
- [ ] Check the box in the top-level `README.md` progress table

Solution reference is in `solution.py` — try the exercises yourself first; only peek if you're stuck for more than a few minutes.
