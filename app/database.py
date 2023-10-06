
from config import *
from cryptography.fernet import Fernet
import json
from datetime import datetime

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

    # If Journal db exists then backup it
    if JOURNAL_JSON_DB_PATH.exists():
        # Define the backup directory path
        backup_dir = BACKUP_DIR  # Replace with your actual backup directory path
        if not backup_dir.exists():
            backup_dir.mkdir()

        # Create a timestamped backup of the current database
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"backup_{timestamp}.json"
        backup_path = backup_dir / backup_filename

        # Getting the decrypted content of the current database using load_database()
        db_content = load_database(json_filePath=JOURNAL_JSON_DB_PATH)

        # Backup this decrypted content into a json
        with open(backup_path, 'w') as f:
            f.write(json.dumps(db_content, indent=4))

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
    save_database(data={"entries": []}, outputFileName=json_filepath)