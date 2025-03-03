#!/bin/bash
echo "Starting application..."
cd /app
echo "Current directory: $(pwd)"
echo "Python version:"
python --version

echo "Starting FastAPI application with Gunicorn..."
gunicorn --bind=0.0.0.0:$PORT --timeout 600 --log-level debug --workers 4 app:app 