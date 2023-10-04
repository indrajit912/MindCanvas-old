"""
Routes and Views

This module defines the routes and views for the Flask web application.

Author: Indrajit Ghosh
Created on: Oct 03, 2023

Attributes:
    app (Flask): The Flask web application instance.
"""

# TODO: Encrypt your json database!

from flask import render_template, request, redirect, url_for, flash
from app import app
from datetime import datetime
import json, pytz
from cryptography.fernet import Fernet
from app.journal import JournalEntry
from config import *

import logging

# Create a logger for the routes module
logger = logging.getLogger(__name__)

    
def load_database(json_filePath):
    """Loads the database"""

    # Get the Fernet key
    key = open(FERNET_FILE, 'rb').read()
    fer = Fernet(key)

    with open(json_filePath, 'rb') as f:
        content_with_header = f.read()
    
    if content_with_header.startswith(b'ENCRYPTED\n'):
        encrypted_content = content_with_header[len(b'ENCRYPTED\n'):]
        json_content = fer.decrypt(encrypted_content).decode()
        content = json.loads(json_content)
    else:
        # If it doesn't have the encryption marker, assume it's plaintext JSON
        with open(json_filePath, 'r') as f:
            content = json.loads(f.read())

    return content  # returns a dictionary


def save_database(data:dict, outputFileName):
    """Saves the dict to the DATABASE_FILE"""

    # Get the Fernet key
    key = open(FERNET_FILE, 'rb').read()
    fer = Fernet(key)

    # Create the json content
    json_content = json.dumps(data, indent=4)

    # Encrypt the content
    encrypted_content = fer.encrypt(json_content.encode())

    # Add a marker/header to indicate that the content is encrypted
    encrypted_content_with_header = b'ENCRYPTED\n' + encrypted_content
    
    with open(outputFileName, 'wb') as f:
        f.write(encrypted_content_with_header)


def create_blank_db(json_filepath):
    """
    Creates a blank json db
        {
            "entries": []
        }
    """
    save_database(data={"entries": [], "encrypted":False}, outputFileName=json_filepath)



######################################################################
#                           Home
######################################################################
@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        str: The rendered HTML template for the index page.
    """
    logger.info('Visited the index route.')
    return render_template('index.html')


# Define a custom Jinja2 filter to format datetime to IST
@app.template_filter('datetimeformat')
def datetimeformat(value:str, format='%b %d, %Y %H:%M:%S %Z'):
    """
    Custom Jinja2 filter to format a datetime object to a specified format.
    Default format is '%Y-%m-%d %H:%M:%S %Z'.

    Args:
        value (datetime): The datetime object to format.
        format (str, optional): The desired format. Defaults to '%Y-%m-%d %H:%M:%S %Z'.

    Returns:
        str: The formatted datetime as a string.
    """
    # Convert the datetime to IST
    ist_timezone = pytz.timezone('Asia/Kolkata')
    dt_time_val = datetime.fromisoformat(value)
    ist_datetime = dt_time_val.astimezone(ist_timezone)

    return ist_datetime.strftime(format)

@app.route('/view_entries')
def view_entries():
    # Load journal entries from the JSON database file
    entries = load_database(JOURNAL_JSON_DB_PATH)['entries']

    return render_template('view_entries.html', entries=entries)


@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    # Create the JSON database file if it doesn't exist
    if not JOURNAL_JSON_DB_PATH.exists():
        create_blank_db(json_filepath=JOURNAL_JSON_DB_PATH)

    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        text = request.form.get('text')

        # Create a new JournalEntry object
        utc_datetime = datetime.utcnow().replace(tzinfo=pytz.utc)
        entry = JournalEntry(title=title, datetime_utc=utc_datetime, text=text)
        
        entries = load_database(JOURNAL_JSON_DB_PATH)['entries']

        # Append the new entry to the existing entries
        entries.append(entry.to_dict())

        # Save the updated entries back to the JSON database
        save_database(data={"entries":entries}, outputFileName=JOURNAL_JSON_DB_PATH)
        # Redirect to the page that displays the entries
        return redirect(url_for('view_entries'))

    return render_template('add_entry.html')


@app.route('/view_entry/<int:entry_id>')
def view_entry(entry_id):
    # Retrieve the journal entry with the specified entry_id from your data source
    # Create the JSON database file if it doesn't exist
    if not JOURNAL_JSON_DB_PATH.exists():
        create_blank_db(json_filepath=JOURNAL_JSON_DB_PATH)

    # Load journal entries from the JSON database file
    entries_data = load_database(JOURNAL_JSON_DB_PATH)
    entries = entries_data['entries']

    # Check if the entry_id is valid
    if entry_id < 0 or entry_id >= len(entries):
        # Handle the case of an invalid entry_id (e.g., display an error message or redirect)
        return "Invalid Entry ID"

    entry = entries[entry_id]

    if entry is None:
        # Handle the case when the entry with the given ID does not exist
        return "Entry not found", 404

    return render_template('view_entry.html', entry=entry, entry_id=entry_id)


@app.route('/update_entry/<int:entry_id>', methods=['GET', 'POST'])
def update_entry(entry_id):
    # Create the JSON database file if it doesn't exist
    if not JOURNAL_JSON_DB_PATH.exists():
        create_blank_db(json_filepath=JOURNAL_JSON_DB_PATH)

    # Load journal entries from the JSON database file
    entries_data = load_database(JOURNAL_JSON_DB_PATH)
    entries = entries_data['entries']

    # Check if the entry_id is valid
    if entry_id < 0 or entry_id >= len(entries):
        # Handle the case of an invalid entry_id (e.g., display an error message or redirect)
        return "Invalid Entry ID"

    entry = JournalEntry.from_dict(entries[entry_id])

    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        text = request.form.get('text')

        # Update the JournalEntry object
        entry._title = title
        entry._text = text

        # Update the entry in the entries list
        entries[entry_id] = entry.to_dict()

        # Save the updated entries back to the JSON database
        entries_data['entries'] = entries
        save_database(data=entries_data, outputFileName=JOURNAL_JSON_DB_PATH)

        # Redirect to the page that displays the updated entries
        return redirect(url_for('view_entries'))

    return render_template('update_entry.html', entry=entry)


@app.route('/delete_entry/<int:entry_id>')
def delete_entry(entry_id):
    # Create the JSON database file if it doesn't exist
    if not JOURNAL_JSON_DB_PATH.exists():
        create_blank_db(json_filepath=JOURNAL_JSON_DB_PATH)

    # Load journal entries from the JSON database file
    entries_data = load_database(JOURNAL_JSON_DB_PATH)
    entries = entries_data['entries']

    # Check if the entry_id is valid
    if entry_id < 0 or entry_id >= len(entries):
        # Flash an error message and redirect to the home page
        flash("Invalid Entry ID", "error")
        return redirect(url_for('home'))

    # Delete the entry with the specified entry_id
    entries.pop(entry_id)

    # Save the updated entries back to the JSON database
    entries_data = {"entries": entries}
    save_database(data=entries_data, outputFileName=JOURNAL_JSON_DB_PATH)

    # Flash a success message and redirect to the home page
    flash("Entry Deleted Successfully", "success")
    entries = load_database(JOURNAL_JSON_DB_PATH)['entries']
    return render_template('entry_deleted.html', entries=entries)
