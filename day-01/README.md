# Day 1 — LLM APIs: talking to Claude directly in Python

**Time budget:** ~1.5 hours
**Prereqs:** the one-time setup in the top-level README (venv + API key in `.env`)

## Why this matters

Everything you've built at ICS MUNI with Copilot Studio and Custom Connectors already talks to an LLM — but Copilot Studio wraps the call for you: it manages the conversation, the prompt template, the retries. Today you remove that wrapper and make the raw call yourself. Once you've done this a few times, tools like LangChain (Week 3) will read as "the same raw call, with conveniences bolted on" instead of magic.

## Core concept: what actually happens in an API call

A call to an LLM API is just an HTTP request. You send:

- **`model`** — which model to run (e.g. `claude-sonnet-4-5-20250929`). Model names are versioned strings; check console.anthropic.com/docs for the current list if a name stops working.
- **`messages`** — a list of turns, each with a `role` (`"user"` or `"assistant"`) and `content` (the text). Today you'll only ever send one `user` message — no history yet, that's Day 3.
- **`system`** *(optional)* — instructions that shape the assistant's behavior, kept separate from the conversation itself. Note: for Claude this is a top-level parameter, not a message with `role: "system"` like some other APIs use — worth noticing since you'll likely meet both conventions.
- **`max_tokens`** — hard cap on how long the response can be. Required by the Anthropic API (no default).
- **`temperature`** *(optional, 0–1)* — how much randomness to inject into token selection. 0 ≈ deterministic/focused, 1 ≈ more varied/creative.

You get back a response object containing the generated text plus metadata — notably `usage` (input/output token counts), which is what you're billed on.

**Analogy:** think of `messages` + `system` as the payload you'd configure in a Custom Connector's request body, and the response's `usage` block as the metering data behind API costs — same shape of problem, one layer lower.

## Exercises

Open `exercise.py`. It has 4 `TODO` sections — do them in order, run the script after each one to see the effect.

1. **Basic call.** Send a single user message ("Explain what an API is, in 2 sentences.") and print `response.content[0].text`.
2. **Add a system prompt.** Set `system="You are a terse, no-nonsense senior engineer. Answer in one sentence."` on the same call and compare the output.
3. **Temperature comparison.** Call the *same* prompt twice — once with `temperature=0`, once with `temperature=1` — and print both responses side by side. Run it 2–3 times. What do you notice about consistency at each setting?
4. **Token usage.** Print `response.usage.input_tokens` and `response.usage.output_tokens` for one of your calls.

## Stretch goal (optional, if you have time left)

Turn the script into a tiny one-shot CLI: read a prompt from `input()`, send it, print the response — no history kept (each call is independent). This is intentionally *not* a chatbot yet; you'll add memory of the conversation on Day 3, and you'll feel exactly why it's needed once you try asking a follow-up question here and watch Claude have no idea what you're referring to.

## Reflection questions (answer these to yourself, or jot notes in `NOTES.md`)

- Why does Claude keep `system` separate from `messages` instead of just making it the first message? What would break if it were just prepended to the conversation?
- If you were charged per token, which of your 4 exercises was the most expensive, and why?
- At `temperature=0`, is the output *guaranteed* to be identical every time? (Try it and see — then think about why the answer is what it is.)

## Done when

- [x] All 4 TODOs in `exercise.py` run without errors
- [x] You can explain in your own words: what `system` does, what `max_tokens` caps, and what `temperature` controls
- [x] You've answered the 3 reflection questions
- [x] Check the box in the top-level `README.md` progress table

Solution reference is in `solution.py` — try the exercises yourself first; only peek if you're stuck for more than a few minutes.
