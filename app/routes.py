"""
Routes and Views

This module defines the routes and views for the Flask web application.

Author: Indrajit Ghosh
Created on: Oct 03, 2023

Attributes:
    app (Flask): The Flask web application instance.
"""

from flask import render_template, request, redirect, url_for, flash
from app import app
from datetime import datetime
import pytz, logging
from cryptography.fernet import Fernet
from app.journal import JournalEntry
from app.database import *
from config import *
from werkzeug.routing import UUIDConverter
import uuid

# Create a logger for the routes module
logger = logging.getLogger(__name__)

# TODO: Add admin login to all routes.

# Register the UUID converter
app.url_map.converters['uuid'] = UUIDConverter

if not FERNET_FILE.exists():
        # Generate a new key and save it
        key = Fernet.generate_key()

        # Save the key to the file
        with open(FERNET_FILE, 'wb') as key_file:
            key_file.write(key)
        
        logger.info("Fernet file created with a new fernet key!")

if not JOURNAL_JSON_DB_PATH.exists():
    create_blank_db(json_filepath=JOURNAL_JSON_DB_PATH)
    logger.info("Blank JSON database file created!")


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

    # Reverse the entries to get last added entries first.
    entries = entries[::-1] 

    logger.info('Visited the view_entries route.')
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

        # Log it
        logger.info('Added a new JournalEntry!')

        # Redirect to the page that displays the entries
        return redirect(url_for('view_entries'))

    return render_template('add_entry.html')


@app.route('/view_entry/<uuid:entry_id>')
def view_entry(entry_id):
    # Retrieve the journal entry with the specified entry_id from your data source
    # Create the JSON database file if it doesn't exist
    if not JOURNAL_JSON_DB_PATH.exists():
        create_blank_db(json_filepath=JOURNAL_JSON_DB_PATH)

    # Load journal entries from the JSON database file
    entries_data = load_database(JOURNAL_JSON_DB_PATH)
    entries = entries_data['entries']

    # Check if the entry_id is valid
    entry = None
    for journal_entry in entries:
        if journal_entry.get('id') == str(entry_id):
            entry = journal_entry
            break

    if entry is None:
        # Handle the case when the entry with the given ID does not exist
        return "Entry not found", 404

    logger.info('Viewed one JournalEntry!')
    return render_template('view_entry.html', entry=entry, entry_id=entry_id)


@app.route('/update_entry/<uuid:entry_id>', methods=['GET', 'POST'])
def update_entry(entry_id):
    # Create the JSON database file if it doesn't exist
    if not JOURNAL_JSON_DB_PATH.exists():
        create_blank_db(json_filepath=JOURNAL_JSON_DB_PATH)

    # Load journal entries from the JSON database file
    entries_data = load_database(JOURNAL_JSON_DB_PATH)
    entries = entries_data['entries']

    # Check if the entry_id is valid
    entry = None
    for journal_entry in entries:
        if journal_entry.get('id') == str(entry_id):
            entry = JournalEntry.from_dict(journal_entry)
            break

    if entry is None:
        # Handle the case when the entry with the given ID does not exist
        return "Entry not found", 404

    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        text = request.form.get('text')

        # Update the JournalEntry object
        entry._title = title
        entry._text = text

        # Update the entry in the entries list
        for index, journal_entry in enumerate(entries):
            if journal_entry.get('id') == str(entry_id):
                entries[index] = entry.to_dict()
                break

        # Save the updated entries back to the JSON database
        entries_data['entries'] = entries
        save_database(data=entries_data, outputFileName=JOURNAL_JSON_DB_PATH)

        # Log it
        logger.info('Updated one JournalEntry!')

        # Flash
        flash("Journal Entry updated successfully!")

        # Render the template.
        return render_template('entry_updated.html', entry=entry.to_dict())

    return render_template('update_entry.html', entry=entry)


@app.route('/delete_entry/<uuid:entry_id>')
def delete_entry(entry_id):
    # Create the JSON database file if it doesn't exist
    if not JOURNAL_JSON_DB_PATH.exists():
        create_blank_db(json_filepath=JOURNAL_JSON_DB_PATH)

    # Load journal entries from the JSON database file
    entries_data = load_database(JOURNAL_JSON_DB_PATH)
    entries = entries_data['entries']

    # Check if the entry_id is valid
    entry_index = None
    for index, journal_entry in enumerate(entries):
        if journal_entry.get('id') == str(entry_id):
            entry_index = index
            break

    if entry_index is None:
        # Handle the case when the entry with the given ID does not exist
        return "Entry not found", 404

    # Delete the entry with the specified entry_id
    entries.pop(entry_index)

    # Save the updated entries back to the JSON database
    entries_data['entries'] = entries
    save_database(data=entries_data, outputFileName=JOURNAL_JSON_DB_PATH)

    # Flash the messg
    flash("Entry deleted successfully!")

    # Log it
    logger.info('Deleted a JournalEntry!')

    # Redirect to the page that displays the updated entries
    return render_template('entry_deleted.html')
