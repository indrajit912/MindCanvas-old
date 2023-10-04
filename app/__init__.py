"""
Flask Web App Initialization

This module initializes the Flask web application instance, configures it, and imports the routes and extensions.

Attributes:
    app (Flask): The Flask web application instance.
"""
from flask import Flask
import logging, json
from config import *
from app.api import api
from cryptography.fernet import Fernet
from app.database import create_blank_db

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO (you can adjust this)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',  # Specify the log file name
    filemode='a'  # Append mode, so log entries are added to the existing log file
)

app.config['SECRET_KEY'] = FLASK_SECRET_KEY

if not FERNET_FILE.exists():
    # Generate a new key and save it
    key = Fernet.generate_key()

    # Save the key to the file
    with open(FERNET_FILE, 'wb') as key_file:
        key_file.write(key)
        
if not JOURNAL_JSON_DB_PATH.exists():
    create_blank_db(json_filepath=JOURNAL_JSON_DB_PATH)

if not ADMIN_JSON_FILE.exists():
        # Save the dictionary to a JSON file with indentation
        with open(ADMIN_JSON_FILE, 'w', encoding='utf-8') as json_file:
            json.dump(DEFAULT_ADMIN, json_file, indent=4)

app.register_blueprint(api, url_prefix='/api')

# Import routes after configuring logging to ensure proper logging in routes.py
from app import routes
