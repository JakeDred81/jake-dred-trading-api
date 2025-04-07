#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Start the Flask app using gunicorn
gunicorn main:app
