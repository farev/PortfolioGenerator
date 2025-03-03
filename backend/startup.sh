#!/bin/bash
echo "Starting application in Azure App Service..."
cd /home/site/wwwroot
echo "Current directory: $(pwd)"
echo "Python version:"
python --version

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Starting FastAPI application with Gunicorn..."
export PORT=${PORT:-8000}
gunicorn --bind=0.0.0.0:$PORT --timeout 600 --log-level debug --workers 4 app:app 