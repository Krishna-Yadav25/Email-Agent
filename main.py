from dotenv import load_dotenv
from groq import Groq
from agents.classifier import classify_email
from agents.responder import generate_response

load_dotenv()
client = Groq()

def respond_to_email(email_text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional email assistant. Write polite replies."},
            {"role": "user", "content": f"Reply to this email:\n{email_text}"}
        ]
    )
    return response.choices[0].message.content

email = "Hi, my order #1234 has not arrived yet. It has been 2 weeks."

category = classify_email(email)
print(f"Category: {category}")

reply = generate_response(email, category)
print("\n=== AI Generated Reply ===")
print(reply)