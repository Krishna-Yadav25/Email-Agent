# Autonomous Email Response Agent

An AI-powered email automation system built with Python and Groq LLM that automatically classifies incoming emails and generates professional replies.

## Features
- AI email classification — complaint, inquiry, support, spam
- Automatic professional reply generation based on category
- Human-in-the-loop approval before sending
- SQLite database to store all email history
- REST API with FastAPI and live interactive docs
- Full error handling and logging
- 7 unit tests passing

## Tech Stack
- Python 3.12
- Groq LLM (llama-3.3-70b-versatile) — free AI API
- FastAPI + Uvicorn — REST API server
- SQLite — email history database
- LangChain — AI agent framework
- Pytest — unit testing

## Project Structure
```
email-agent/
├── agents/
│   ├── classifier.py     # Classifies email type using AI
│   └── responder.py      # Generates AI reply based on category
├── database/
│   └── db.py             # SQLite save and fetch operations
├── tests/
│   ├── test_classifier.py
│   └── test_db.py
├── api.py                # FastAPI REST endpoints
├── main.py               # Run from terminal
├── conftest.py           # Pytest configuration
└── requirements.txt
```

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Krishna-Yadav25/Email-Agent.git
cd Email-Agent
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**3. Install packages**
```bash
pip install -r requirements.txt
```

**4. Add API key**

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at console.groq.com

## Run

**Terminal mode — process sample emails:**
```bash
python main.py
```

**API mode — start REST server:**
```bash
uvicorn api:app --reload
```

**Run tests:**
```bash
pytest tests/ -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check |
| POST | /process-email | Classify and reply to email |
| GET | /emails | View all stored emails |

## API Docs
Visit `http://127.0.0.1:8000/docs` for live interactive documentation.

## Architecture
```
Incoming Email
      ↓
Classifier Agent (Groq AI)
      ↓
Category: complaint / inquiry / support / spam
      ↓
Responder Agent (Groq AI)
      ↓
Professional Reply Generated
      ↓
Saved to SQLite Database
```