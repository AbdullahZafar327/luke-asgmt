# Business Agent Card Generator

A web app that takes any public business URL, scans it, builds a structured **Business Map**, and generates a machine-readable **Agent Card** that AI agents can use to understand and interact with the business.

---

## How it works

1. User enters a business URL and clicks **Analyze**
2. The scraper crawls up to 2 pages using Crawl4AI
3. Deterministic extraction pulls forms, links, contact info, and third-party tools
4. An LLM generates a **Business Map** from the extracted evidence
5. The same LLM generates an **Agent Card** from the Business Map (not from raw data)
6. Both are displayed in the frontend

---

## Project Structure

```
luke-asgmt/
├── backend/         # Python + FastAPI
│   ├── main.py
│   ├── scraper.py
│   ├── extractor.py
│   ├── business_map.py
│   ├── agent_card.py
│   ├── llm.py
│   └── pyproject.toml
└── fronted/         # Next.js + Tailwind
    ├── src/
    │   ├── app/
    │   │   └── page.tsx
    │   └── components/
    │       ├── UrlInput.tsx
    │       ├── BusinessMap.tsx
    │       └── AgentCard.tsx
    └── package.json
```

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- [uv](https://github.com/astral-sh/uv) — Python package manager
- [Ollama](https://ollama.com) — for running the LLM locally

---

## 1. Install and run Ollama

### Install

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: download from https://ollama.com/download
```

### Pull the model

```bash
ollama pull llama3.2
```

### Run Ollama

Just open the **Ollama app** from your Applications folder. It runs in the menu bar automatically.

Or from terminal:

```bash
ollama serve
```

Ollama runs at `http://localhost:11434`.

---

## 2. Run the backend

```bash
cd backend

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Install Playwright browser (required by Crawl4AI, first time only)
playwright install chromium

# Create environment file
cp .env.example .env
# Edit .env and set LLM_PROVIDER=ollama
```

### `.env` file

```env
# Local development — uses Ollama
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434

# Production — switch to Claude (get key from interviewer)
# LLM_PROVIDER=claude
# ANTHROPIC_API_KEY=sk-ant-...
```

### Start the backend

```bash
uv run uvicorn main:app --reload --port 8000
```

Backend runs at `http://localhost:8000`.

---

## 3. Run the frontend

```bash
cd fronted

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at `http://localhost:3000`.

---

## Running everything together

You need **3 terminals**:

| Terminal | Command |
|----------|---------|
| 1 — Ollama | Open Ollama app (menu bar) |
| 2 — Backend | `cd backend && source .venv/bin/activate && uv run uvicorn main:app --reload --port 8000` |
| 3 — Frontend | `cd fronted && npm run dev` |

Then open `http://localhost:3000` in your browser.

---

## Switching to Claude API (for presentation)

When you have a Claude API key, update `backend/.env`:

```env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Restart the backend. No other changes needed — same prompts, same output format.

---

## Testing the backend directly

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.sweetgreen.com"}'
```

### Test the LLM connection only

```bash
cd backend
source .venv/bin/activate
uv run test_llm.py
```

---

## Example outputs

Tested on:
- `https://www.sweetgreen.com` — restaurant chain
- `https://calendly.com` — SaaS scheduling tool
- `https://example.com` — minimal site (shows unknown handling)

---

## Architecture

| Step | What runs | Technology |
|------|-----------|------------|
| Scraping | Crawl4AI async crawler | Python |
| Extraction | Forms, links, contact, third-party scripts | BeautifulSoup + regex (deterministic) |
| Business Map | LLM prompt with evidence | LangChain + Ollama / Claude |
| Agent Card | LLM prompt from Business Map only | LangChain + Ollama / Claude |
| API | REST endpoint | FastAPI |
| Frontend | UI with two-layer output | Next.js + Tailwind CSS |

The key design principle: **the Agent Card is always generated from the Business Map, never directly from raw scraped data.** This ensures the card is grounded in verified evidence and unknowns are explicitly marked.