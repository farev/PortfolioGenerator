#!/bin/bash
echo "Starting custom startup script"

# Skip virtual environment creation and directly install packages
echo "Installing dependencies..."
python -m pip install --user --upgrade pip
python -m pip install --user -r /home/site/wwwroot/requirements.txt

# Start the application
echo "Starting application with Gunicorn..."
cd /home/site/wwwroot
python3 -m gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 4 app:app 