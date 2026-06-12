import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
client = Groq()

def generate_response(email_text, category):
    try:
        logger.info(f"Generating response for category: {category}")
        tone_map = {
            "complaint": "very apologetic and solution-focused",
            "inquiry": "helpful and informative",
            "support": "technical and step-by-step",
            "spam": "do not reply",
            "other": "professional and polite"
        }
        tone = tone_map.get(category, "professional")

        if category == "spam":
            logger.warning("Spam email detected - skipping reply")
            return "SKIP - Spam email detected"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are a professional email assistant. Be {tone}."},
                {"role": "user", "content": f"Reply to this email:\n{email_text}"}
            ]
        )
        reply = response.choices[0].message.content
        logger.info("Response generated successfully")
        return reply
    except Exception as e:
        logger.error(f"Response generation failed: {e}")
        return "Sorry, we could not process your email right now. Please try again later."