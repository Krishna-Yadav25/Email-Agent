import logging
from dotenv import load_dotenv
from agents.classifier import classify_email
from agents.responder import generate_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
load_dotenv()

def process_email(email_text):
    logger.info("=== Starting email processing ===")
    try:
        category = classify_email(email_text)
        print(f"\n Category Detected: {category.upper()}")

        reply = generate_response(email_text, category)
        print(f"\n=== AI Generated Reply ===")
        print(reply)

        logger.info("=== Email processing complete ===")
        return {"category": category, "reply": reply}

    except Exception as e:
        logger.error(f"Email processing failed: {e}")
        return {"category": "error", "reply": "System error occurred"}

emails = [
    "Hi, my order #1234 has not arrived yet. It has been 2 weeks.",
    "Buy cheap medicines now! Click here!!!",
    "Can you explain how your refund policy works?"
]

for i, email in enumerate(emails, 1):
    print(f"\n{'='*50}")
    print(f"EMAIL {i}: {email}")
    process_email(email)