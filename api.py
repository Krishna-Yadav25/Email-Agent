import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from agents.classifier import classify_email
from agents.responder import generate_response
from database.db import init_db, save_email, get_all_emails
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Email Response Agent", version="1.0.0")
init_db()

class EmailRequest(BaseModel):
    email_text: str

class EmailResponse(BaseModel):
    category: str
    reply: str

@app.get("/")
def home():
    return {"message": "Email Agent API is running!"}

@app.post("/process-email", response_model=EmailResponse)
def process_email(request: EmailRequest):
    try:
        category = classify_email(request.email_text)
        reply = generate_response(request.email_text, category)
        save_email(request.email_text, category, reply)
        return EmailResponse(category=category, reply=reply)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/emails")
def get_emails():
    emails = get_all_emails()
    return {"total": len(emails), "emails": emails}