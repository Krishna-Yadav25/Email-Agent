import pytest
import os
import sqlite3
from database.db import init_db, save_email, get_all_emails

TEST_DB = "test_emails.db"

def setup_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def teardown_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_init_db_creates_table(monkeypatch):
    monkeypatch.setattr('database.db.DB_PATH', TEST_DB)
    init_db()
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emails'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None

def test_save_and_retrieve_email(monkeypatch):
    monkeypatch.setattr('database.db.DB_PATH', TEST_DB)
    init_db()
    save_email("Test email body", "inquiry", "Test reply")
    emails = get_all_emails()
    assert len(emails) == 1
    assert emails[0][1] == "Test email body"
    assert emails[0][2] == "inquiry"

def test_multiple_emails_saved(monkeypatch):
    monkeypatch.setattr('database.db.DB_PATH', TEST_DB)
    init_db()
    save_email("Email 1", "complaint", "Reply 1")
    save_email("Email 2", "inquiry", "Reply 2")
    save_email("Email 3", "spam", "SKIP")
    emails = get_all_emails()
    assert len(emails) == 3