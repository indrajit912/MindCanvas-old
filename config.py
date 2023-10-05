"""
Flask App Configuration

This module defines configuration settings for the Flask web application.

"""
import os
from os.path import join, dirname
from dotenv import load_dotenv
from pathlib import Path

DOT_ENV_FILE = join(dirname(__file__), '.env')
load_dotenv(DOT_ENV_FILE)


BASE_DIR = Path(__file__).resolve().parent
JOURNAL_JSON_DB_PATH = BASE_DIR / 'journal_entries.json'
BACKUP_DIR = BASE_DIR / "backups"
FLASK_SECRET_KEY = "Hdksfol324khkj"

FERNET_FILE = BASE_DIR / '.fernetkey'

ADMIN_JSON_FILE = BASE_DIR / 'admin.json'

DEFAULT_ADMIN = {
    "admin_username": "admin",
    "admin_password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # SHA256('password')
    "salt": ''
}
