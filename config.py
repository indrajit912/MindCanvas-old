"""
Flask App Configuration

This module defines configuration settings for the Flask web application.

"""
import os
from os.path import join, dirname
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BASE_DIR = Path(__file__).resolve().parent
JOURNAL_JSON_DB_PATH = BASE_DIR / 'journal_entries.json'
FLASK_SECRET_KEY = "Hdksfol324khkj"

FERNET_FILE = BASE_DIR / '.fernetkey'

# Predefined admin credentials (change these to your actual credentials)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'