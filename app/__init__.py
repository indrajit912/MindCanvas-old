"""
Flask Web App Initialization

This module initializes the Flask web application instance, configures it, and imports the routes and extensions.

Attributes:
    app (Flask): The Flask web application instance.
"""
from flask import Flask
import logging
from config import *

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO (you can adjust this)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',  # Specify the log file name
    filemode='a'  # Append mode, so log entries are added to the existing log file
)

app.config['SECRET_KEY'] = FLASK_SECRET_KEY

# Import routes after configuring logging to ensure proper logging in routes.py
from app import routes
