#!/bin/bash
echo "Starting custom startup script"

# Create log directory if it doesn't exist
mkdir -p /home/LogFiles/python

# Install dependencies directly (no virtual env)
echo "Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r /home/site/wwwroot/requirements.txt

# Print Python version and installed packages for debugging
echo "Python version:"
python --version
echo "Installed packages:"
pip list

# Start the application
echo "Starting application with Gunicorn..."
cd /home/site/wwwroot
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 4 app:app 2>&1 | tee /home/LogFiles/python/gunicorn.log 