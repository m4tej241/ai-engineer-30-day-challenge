# AI Engineer 30-Day Challenge

Goal: build the practical skills and a portfolio project to demonstrate AI engineering competency for job applications (Brno-based, open to Warsaw/Vienna/Berlin/Amsterdam/London).

Pace: ~1.5 hours/day. Each day has its own folder with a `README.md` (concepts + exercises), starter code, and a reference solution.

## Week 1 — AI-in-Python essentials

| Day | Topic | Status |
|---|---|---|
| 1 | LLM APIs — talking to Claude directly in Python | ✅ done |
| 2 | Streaming responses | ✅ done |
| 3 | Multi-turn chat (conversation state) | ⬜ |
| 4 | Pydantic for structured outputs | ⬜ |
| 5 | Embeddings | ⬜ |
| 6–7 | ChromaDB + semantic search mini-project | ⬜ |

## Week 2 — LLM fundamentals and RAG

Chunking strategies, vector storage, retrieval, full RAG pipeline. (Detailed day-by-day plan to be added when we get there.)

## Week 3 — Agents and tools with LangChain

## Week 4 — Full portfolio project, deployed via Streamlit Cloud

---

### Setup (one-time, do this before Day 1)

```bash
cd ai-engineer-30-day-challenge
python3 -m venv .venv
source .venv/bin/activate
pip install -r day-01/requirements.txt
cp day-01/.env.example .env
# then edit .env and paste your Anthropic API key (get one at console.anthropic.com)
```

Keep reusing this same `.venv` across the whole challenge — each day's `requirements.txt` just adds to it.
