# 🤖 Autonomous Email Response Agent

> An AI-powered email automation system that classifies incoming emails and generates professional replies automatically — deployed live on the internet.

**Live Demo:** [email-agent-production-be32.up.railway.app](https://email-agent-production-be32.up.railway.app)  
**API Docs:** [email-agent-production-be32.up.railway.app/docs](https://email-agent-production-be32.up.railway.app/docs)

---

## Features

- AI email classification — complaint, inquiry, support, spam, other
- Automatic professional reply generation based on email category
- Gmail inbox integration with human-in-the-loop approval
- Beautiful web interface — paste any email and get an AI reply instantly
- REST API with FastAPI and live interactive documentation
- SQLite database to store all processed email history
- Full error handling and structured logging
- 7 unit tests — all passing
- Deployed live on Railway (24/7)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| AI Model | Groq LLM (llama-3.3-70b-versatile) |
| API Framework | FastAPI + Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Gmail Integration | Google Gmail API + OAuth2 |
| Testing | Pytest |
| Deployment | Railway |
| Version Control | Git + GitHub |

---

## Project Structure

```
email-agent/
├── agents/
│   ├── __init__.py
│   ├── classifier.py        # Classifies email type using Groq AI
│   └── responder.py         # Generates AI reply based on category
├── database/
│   ├── __init__.py
│   └── db.py                # SQLite save and fetch operations
├── static/
│   └── index.html           # Beautiful web interface
├── tests/
│   ├── __init__.py
│   ├── test_classifier.py   # Unit tests for classifier
│   └── test_db.py           # Unit tests for database
├── utils/
│   ├── __init__.py
│   └── gmail_utils.py       # Gmail API read/send/mark functions
├── api.py                   # FastAPI REST endpoints
├── gmail_agent.py           # Gmail inbox automation agent
├── main.py                  # Terminal mode runner
├── conftest.py              # Pytest configuration
├── requirements.txt
├── Procfile                 # Railway deployment config
└── .gitignore
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/Krishna-Yadav25/Email-Agent.git
cd Email-Agent
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate.bat

# Mac/Linux
source venv/bin/activate
```

### 3. Install packages
```bash
pip install -r requirements.txt
```

### 4. Create .env file
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at [console.groq.com](https://console.groq.com)

---

## Run

### Web API mode
```bash
uvicorn api:app --reload
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) for the web interface.  
Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for API docs.

### Terminal mode
```bash
python main.py
```

### Gmail agent mode
```bash
python gmail_agent.py
```
First run opens browser for Gmail OAuth sign-in.

### Run tests
```bash
pytest tests/ -v
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Web interface |
| POST | /process-email | Classify and reply to email |
| GET | /emails | View all stored emails |
| GET | /docs | Interactive API documentation |

### Example API request
```bash
curl -X POST https://email-agent-production-be32.up.railway.app/process-email \
  -H "Content-Type: application/json" \
  -d '{"email_text": "My order has not arrived yet. Please help."}'
```

### Example response
```json
{
  "category": "complaint",
  "reply": "Dear Customer, I sincerely apologize for the delay..."
}
```

---

## Email Categories

| Category | Tone of Reply |
|---|---|
| Complaint | Very apologetic, solution-focused |
| Inquiry | Helpful, informative |
| Support | Technical, step-by-step |
| Spam | Auto-skipped, no reply generated |
| Other | Professional and polite |

---

## Architecture

```
User pastes email
      ↓
Classifier Agent (Groq AI)
      ↓
Category detected
      ↓
Responder Agent (Groq AI)
      ↓
Professional reply generated
      ↓
Saved to SQLite Database
      ↓
Returned to user / sent via Gmail
```

---

## Gmail Integration

The Gmail agent reads your real inbox and processes emails automatically:

1. Connects to Gmail via OAuth2 (sign in once, token saved)
2. Fetches unread emails (max 5 at a time)
3. Classifies each email using AI
4. Generates a professional reply
5. Shows you the reply for approval — Send, Edit, or Skip
6. Sends the reply and marks email as read
7. Saves everything to the database

---

## Test Results

```
tests/test_classifier.py::test_classify_complaint           PASSED
tests/test_classifier.py::test_classify_spam                PASSED
tests/test_classifier.py::test_classify_inquiry             PASSED
tests/test_classifier.py::test_classify_returns_other       PASSED
tests/test_db.py::test_init_db_creates_table                PASSED
tests/test_db.py::test_save_and_retrieve_email              PASSED
tests/test_db.py::test_multiple_emails_saved                PASSED

7 passed in 1.20s
```

---

## Developer

**Krishna Yadav**   
GitHub: [Krishna-Yadav25](https://github.com/Krishna-Yadav25)