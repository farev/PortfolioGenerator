#!/bin/bash
cd /home/site/wwwroot
# Install dependencies if not already installed
pip install -r requirements.txt
# Start the application
gunicorn --bind=0.0.0.0:$PORT --timeout 600 app:app 