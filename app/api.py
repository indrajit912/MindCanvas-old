import os
import json
from flask import Blueprint, jsonify, send_file, request, Response
from app.database import load_database
from config import JOURNAL_JSON_DB_PATH, BASE_DIR
from app.authentication import verify_token, admin_login_required
from flask import flash, redirect, url_for

api = Blueprint('api', __name__)

@api.route('/export/json/', methods=['GET'])
def export_data():

    token = request.args.get('token')

    if token is None:
        return "Unauthorized access: You need a token", 401
    
    # Verify the token
    if not verify_token(token):
        return "Unauthorized access: Invalid token", 401
    
    data = load_database(JOURNAL_JSON_DB_PATH)

    # Check if the request wants to download the data
    download = request.args.get('download', False)

    if download:
        # Save the data as a JSON file temporarily
        temp_json_filename = BASE_DIR / 'exported_data.json'
        with open(temp_json_filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        # Send the file for download
        response = send_file(
            temp_json_filename,
            as_attachment=True,
            download_name='mindcanvas_data.json',
            mimetype='application/json'
        )

        # Remove the temporary JSON file after sending
        os.remove(temp_json_filename)
        return response
    
    else:
        # If not downloading, return the data as JSON for viewing in the browser
        return jsonify(data)
    

@api.route('/upload/json/', methods=['POST'])
@admin_login_required  # Ensure only admins can access this route
def upload_json_file():
    # Check if a file was submitted in the request
    if 'json_file' not in request.files:
        flash('No file provided', 'error')
        return redirect(url_for('index'))  # Redirect to an admin page

    json_file = request.files['json_file']

    # Check if the file has a valid JSON extension
    if not json_file.filename.endswith('.json'):
        flash('Invalid file format. Please upload a JSON file.', 'error')
        return redirect(url_for('index'))  # Redirect to an admin page

    # Save the uploaded file to the JOURNAL_JSON_DB_PATH location, replacing the existing file
    json_file.save(JOURNAL_JSON_DB_PATH)

    flash('JSON file uploaded and database replaced successfully.', 'success')
    return redirect(url_for('view_entries'))  # Redirect to an admin page