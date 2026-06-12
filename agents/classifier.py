import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
client = Groq()

def classify_email(email_text):
    try:
        logger.info("Classifying email...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Classify this email into exactly ONE category: inquiry, complaint, support, spam, or other. Reply with just the single word, nothing else."},
                {"role": "user", "content": email_text}
            ]
        )
        category = response.choices[0].message.content.strip().lower()
        logger.info(f"Email classified as: {category}")
        return category
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        return "other"