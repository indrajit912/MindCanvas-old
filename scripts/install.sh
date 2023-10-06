#!/bin/bash

# Clone the repository from GitHub
git clone https://github.com/indrajit912/MindCanvas.git

# Change to the project directory
cd MindCanvas

# Install the required dependencies
pip install -r requirements.txt

# Provide a message to the user
echo "Installation successful. To run the app, use the following command:"
echo "python3 run.py"
