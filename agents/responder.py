from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

def generate_response(email_text, category):
    tone_map = {
        "complaint": "very apologetic and solution-focused",
        "inquiry": "helpful and informative",
        "support": "technical and step-by-step",
        "spam": "do not reply, just say SKIP",
        "other": "professional and polite"
    }
    tone = tone_map.get(category, "professional")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"You are a professional email assistant. Be {tone}."},
            {"role": "user", "content": f"Reply to this email:\n{email_text}"}
        ]
    )
    return response.choices[0].message.content