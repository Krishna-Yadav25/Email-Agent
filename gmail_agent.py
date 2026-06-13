import logging
import time
from dotenv import load_dotenv
from utils.gmail_utils import get_gmail_service, get_unread_emails, send_reply, mark_as_read
from agents.classifier import classify_email
from agents.responder import generate_response
from database.db import init_db, save_email

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def ask_approval(email, category, reply):
    print("\n" + "="*60)
    print(f"From    : {email['sender']}")
    print(f"Subject : {email['subject']}")
    print(f"Category: {category.upper()}")
    print("-"*60)
    print(f"AI Reply:\n{reply}")
    print("="*60)
    while True:
        choice = input("\n[S]end  [E]dit  [X]Skip: ").strip().upper()
        if choice == 'S':
            return 'send', reply
        elif choice == 'E':
            print("Type edited reply (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if line == "" and lines:
                    break
                lines.append(line)
            edited = "\n".join(lines)
            if input("Send this? [Y/N]: ").strip().upper() == 'Y':
                return 'send', edited
        elif choice == 'X':
            return 'skip', None

def process_inbox():
    init_db()
    print("Connecting to Gmail...")
    service = get_gmail_service()
    print("Connected! Checking inbox...")
    emails = get_unread_emails(service, max_results=5)
    if not emails:
        print("No unread emails found.")
        return
    print(f"Found {len(emails)} unread emails!")
    for email in emails:
        full_text = f"Subject: {email['subject']}\n{email['body']}"
        category = classify_email(full_text)
        if category == 'spam':
            print(f"Skipping spam from {email['sender']}")
            mark_as_read(service, email['id'])
            continue
        reply = generate_response(full_text, category)
        action, final_reply = ask_approval(email, category, reply)
        if action == 'send':
            if send_reply(service, email, final_reply):
                save_email(full_text, category, final_reply)
                mark_as_read(service, email['id'])
                print("Reply sent and saved!")
        else:
            print("Email skipped.")

if __name__ == "__main__":
    process_inbox()