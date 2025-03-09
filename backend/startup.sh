#!/bin/bash

# Add timestamp to logs
log_with_timestamp() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Create virtual environment if it doesn't exist
if [ ! -d "/home/site/wwwroot/antenv" ]; then
    log_with_timestamp "Creating virtual environment..."
    python -m venv /home/site/wwwroot/antenv
fi

# Activate virtual environment
source /home/site/wwwroot/antenv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
log_with_timestamp "Installing dependencies..."
pip install -r /home/site/wwwroot/requirements.txt

# Start the application
log_with_timestamp "Starting application..."
cd /home/site/wwwroot
gunicorn --config gunicorn.conf.py app:app 