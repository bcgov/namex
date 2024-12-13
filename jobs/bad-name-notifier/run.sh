#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Export environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Run the Flask app
python app.py
