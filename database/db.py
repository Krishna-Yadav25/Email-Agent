import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
DB_PATH = "emails.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_text TEXT NOT NULL,
            category TEXT NOT NULL,
            reply TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Database initialized")

def save_email(email_text, category, reply):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO emails (email_text, category, reply, timestamp) VALUES (?, ?, ?, ?)",
            (email_text, category, reply, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        logger.info("Email saved to database")
    except Exception as e:
        logger.error(f"Failed to save email: {e}")

def get_all_emails():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emails")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Failed to fetch emails: {e}")
        return []