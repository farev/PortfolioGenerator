#!/bin/bash
echo "Starting application..."
cd /home/site/wwwroot
echo "Current directory: $(pwd)"
echo "Listing files:"
ls -la

echo "Installing dependencies again to be safe..."
pip install -r requirements.txt

echo "Starting FastAPI application with Gunicorn..."
gunicorn --bind=0.0.0.0:$PORT --timeout 600 --log-level debug app:app 