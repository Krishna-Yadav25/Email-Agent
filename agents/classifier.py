from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

def classify_email(email_text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Classify this email into exactly ONE category: inquiry, complaint, support, spam, or other. Reply with just the single word category, nothing else."},
            {"role": "user", "content": email_text}
        ]
    )
    return response.choices[0].message.content.strip().lower()