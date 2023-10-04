# app/api.py

from flask import Blueprint, jsonify
from app.database import load_database
from config import JOURNAL_JSON_DB_PATH

api = Blueprint('api', __name__)

@api.route('/export/json/', methods=['GET'])
def export_data():
    data = load_database(JOURNAL_JSON_DB_PATH)
    return jsonify(data)