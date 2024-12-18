#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Export environment variables
export FLASK_APP=src/app.py
export FLASK_ENV=development

# Run the Flask app
python src/app.py
