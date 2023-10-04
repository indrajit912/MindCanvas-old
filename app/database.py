
from config import *
from cryptography.fernet import Fernet
import json

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