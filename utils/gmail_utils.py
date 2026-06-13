import os
import base64
import logging
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_unread_emails(service, max_results=5):
    try:
        results = service.users().messages().list(
            userId='me', labelIds=['INBOX'],
            q='is:unread', maxResults=max_results
        ).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(
                userId='me', id=msg['id'], format='full'
            ).execute()
            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            body = extract_body(msg_data['payload'])
            emails.append({
                'id': msg['id'],
                'thread_id': msg_data['threadId'],
                'subject': subject,
                'sender': sender,
                'body': body
            })
        return emails
    except Exception as e:
        logger.error(f"Failed to fetch emails: {e}")
        return []

def extract_body(payload):
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                body = base64.urlsafe_b64decode(data).decode('utf-8')
                break
    elif 'body' in payload:
        data = payload['body'].get('data', '')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')
    return body

def send_reply(service, original_email, reply_text):
    try:
        message = MIMEText(reply_text)
        message['to'] = original_email['sender']
        message['subject'] = f"Re: {original_email['subject']}"
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        service.users().messages().send(
            userId='me',
            body={'raw': raw, 'threadId': original_email['thread_id']}
        ).execute()
        logger.info(f"Reply sent to {original_email['sender']}")
        return True
    except Exception as e:
        logger.error(f"Failed to send reply: {e}")
        return False

def mark_as_read(service, email_id):
    try:
        service.users().messages().modify(
            userId='me', id=email_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
    except Exception as e:
        logger.error(f"Failed to mark as read: {e}")