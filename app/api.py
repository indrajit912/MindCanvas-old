import os
import json
from flask import Blueprint, jsonify, send_file, request, Response
from app.database import load_database
from config import JOURNAL_JSON_DB_PATH, BASE_DIR

api = Blueprint('api', __name__)

@api.route('/export/json/', methods=['GET'])
def export_data():
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
