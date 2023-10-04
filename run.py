# Mindcanvas
#
# Author: Indrajit Ghosh
# Created on: Oct 03, 2023
#

"""
Run Flask Web App

This script starts the Flask development server to run the web application.

Usage:
    python run.py

Note:
    Make sure you have the necessary dependencies installed and the virtual environment activated.

"""

from app import app
import webbrowser
from waitress import serve
from config import *
from app.routes import create_blank_db
from cryptography.fernet import Fernet

def main():
    if not FERNET_FILE.exists():
        # Generate a new key and save it
        key = Fernet.generate_key()

        # Save the key to the file
        with open(FERNET_FILE, 'wb') as key_file:
            key_file.write(key)

    if not JOURNAL_JSON_DB_PATH.exists():
        create_blank_db(json_filepath=JOURNAL_JSON_DB_PATH)

    
    # webbrowser.open("http://0.0.0.0:5000/")
    # serve(app, port=5000)

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
    