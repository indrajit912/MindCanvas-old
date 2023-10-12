"""
Routes and Views

This module defines the routes and views for the Flask web application.

Author: Indrajit Ghosh
Created on: Oct 03, 2023

Attributes:
    app (Flask): The Flask web application instance.
"""

from flask import render_template, request, redirect, url_for, flash, session
from app import app
from datetime import datetime
import pytz, logging
from app.journal import JournalEntry
from app.database import *
from config import *
from werkzeug.routing import UUIDConverter
from app.authentication import user_login_successful, save_new_admin_credentials, generate_token, admin_login_required

# Create a logger for the routes module
logger = logging.getLogger(__name__)

# Register the UUID converter
app.url_map.converters['uuid'] = UUIDConverter


# Route for the admin login page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if user_login_successful(username=username, password=password):
            logger.info("Admin login successful!")

            # Generate a token for the user upon successful login
            token = generate_token(username)

            session['token'] = token
            session['admin_logged_in'] = True

            flash(
                category="info",
                message=f"Successfully logged in as administrator! Now you can visit all tabs."
            )
            return redirect(url_for('index'))
        else:
            flash(message="Wrong username or password!", category="error")  # Flash the message only on login failure

    return render_template('admin_login.html')


@app.route('/update_credentials', methods=['GET', 'POST'])
def update_credentials():
    if request.method == 'POST':
        old_username = request.form['old_username']
        old_password = request.form['old_password']
        new_username = request.form['new_username']
        new_password = request.form['new_password']

        # Check if old credentials are correct
        if user_login_successful(username=old_username, password=old_password):
            # Update the admin username and/or password
            new_password = None if new_password == '' else new_password
            new_username = None if new_username == '' else new_username
            save_new_admin_credentials(new_username=new_username, new_password=new_password)

            flash(
                message="Credentials updated successfully!", 
                category="success"
            )
            return redirect(url_for('admin_login'))
        else:
            flash(
                message="Incorrect old credentials. Please try again.",
                category="error"
            )

    return render_template('update_credentials.html')


######################################################################
#                           Routes
######################################################################
@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        str: The rendered HTML template for the index page.
    """
    return render_template('index.html')


# Define the route for 'upload_db'
@app.route('/upload_database', methods=['GET'])
def upload_database():
    return render_template('upload_database.html')
    

# Define a custom Jinja2 filter to format datetime to IST
@app.template_filter('datetimeformat')
def datetimeformat(value:str, format='%b %d, %Y %I:%M:%S %p %Z'):
    """
    Custom Jinja2 filter to format a datetime object to a specified format.
    Default format is '%Y-%m-%d %H:%M:%S %Z'.

    Args:
        value (datetime): The datetime object to format.
        format (str, optional): The desired format. Defaults to '%b %d, %Y %I:%M:%S %p %Z'.

    Returns:
        str: The formatted datetime as a string.
    """
    # Convert the datetime to IST
    ist_timezone = pytz.timezone('Asia/Kolkata')
    dt_time_val = datetime.fromisoformat(value)
    ist_datetime = dt_time_val.astimezone(ist_timezone)

    return ist_datetime.strftime(format)

@app.route('/view_entries')
@admin_login_required
def view_entries():
    # Load journal entries from the JSON database file
    entries = load_database(JOURNAL_JSON_DB_PATH)['entries']

    # Reverse the entries to get last added entries first.
    entries = entries[::-1] # list of dicts
    total_entries = len(entries)

    logger.info('Visited the view_entries route.')
    return render_template('view_entries.html', entries=entries, total_entries=total_entries)


@app.route('/add_entry', methods=['GET', 'POST'])
@admin_login_required
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

        # Flash message
        flash(
            category="success",
            message="JournalEntry added successfully!"
        )

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
@admin_login_required
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
        flash(
            category="success",
            message="Journal Entry updated successfully!"
        )

        # Render the template.
        return render_template('entry_updated.html', entry=entry.to_dict())

    return render_template('update_entry.html', entry=entry)


@app.route('/delete_entry/<uuid:entry_id>')
@admin_login_required
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
    flash(
        category="success",
        message="Entry deleted successfully!"
    )

    # Log it
    logger.info('Deleted a JournalEntry!')

    # Redirect to the page that displays the updated entries
    return redirect(url_for('view_entries'))
