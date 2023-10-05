# app/authentication.py
# Author: Indrajit Ghosh
# Created On: Oct 04, 2023

from config import *
import json, hashlib, secrets
from itsdangerous import URLSafeSerializer, BadSignature
from flask import session, redirect, url_for
from functools import wraps

# Initialize the serializer
serializer = URLSafeSerializer(FLASK_SECRET_KEY)

# Function to generate a token for a user
def generate_token(username):
    return serializer.dumps(username)

def verify_token(token):
    try:
        # Attempt to load and verify the token
        username = serializer.loads(token)
        return True  # Token is valid
    except BadSignature:
        return False  # Token is invalid

def sha256_hash(raw_text):
    """Return the hex hash value"""
    hashed = hashlib.sha256(raw_text.encode()).hexdigest()
    return hashed

def generate_random_salt(length:int=16):
    """Generates a random salt"""
    # Generate a random salt of a specific length (e.g., 16 bytes)
    salt = secrets.token_bytes(length)
    return salt.hex()


######################################################################
#                          Admin Login
######################################################################

# Custom decorator to force login
def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if 'admin_logged_in' in session and session['admin_logged_in']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('admin_login'))
    return decorated_view

def user_login_successful(username, password):
    """Returns Bool"""
    if not ADMIN_JSON_FILE.exists():
        # Save the dictionary to a JSON file with indentation
        with open(ADMIN_JSON_FILE, 'w', encoding='utf-8') as json_file:
            json.dump(DEFAULT_ADMIN, json_file, indent=4)
    
    # Later, you can load the JSON file and convert it back to a dictionary
    with open(ADMIN_JSON_FILE, 'r', encoding='utf-8') as json_file:
        admin_data = json.load(json_file)

    admin_username = admin_data['admin_username']
    admin_password_hash = admin_data['admin_password_hash']
    admin_salt = admin_data['salt']

    return username == admin_username and sha256_hash(password + admin_salt) == admin_password_hash

def save_new_admin_credentials(new_username=None, new_password=None):
    """
    This function loads ADMIN_JSON_FILE, reads the dictionary inside it into a variable `old_admin_data`.
    Then it generates a new `salt` using `generate_random_salt()` if `new_password` is not None.
    Then it does the following:
        1. old_admin_data['admin_username'] = new_username if new_username is not None
        2. old_admin_data['admin_password_hash'] = sha256_hash(new_password + salt) if new_password is not None
        3. old_admin_data['salt'] = salt
    Finally, it saves the updated `old_admin_data` back to the ADMIN_JSON_FILE.

    :param new_username: The new username to set (optional)
    :param new_password: The new password to set (optional)
    """
    # Load existing admin data from the JSON file
    try:
        with open(ADMIN_JSON_FILE, 'r') as json_file:
            old_admin_data = json.load(json_file)
    except FileNotFoundError:
        old_admin_data = DEFAULT_ADMIN

    # Generate a new salt if a new password is provided
    salt = generate_random_salt() if new_password is not None else None

    # Update admin data if new values are provided
    if new_username is not None:
        old_admin_data['admin_username'] = new_username
    if new_password is not None:
        # Hash the new password with the salt
        password_hash = sha256_hash(new_password + salt)
        old_admin_data['admin_password_hash'] = password_hash
        old_admin_data['salt'] = salt

    # Save the updated admin data to the JSON file
    with open(ADMIN_JSON_FILE, 'w') as json_file:
        json.dump(old_admin_data, json_file, indent=4)