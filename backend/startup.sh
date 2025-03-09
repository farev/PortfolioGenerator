#!/bin/bash

# Add timestamp to logs
log_with_timestamp() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Check Python version
PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ $(echo "$PYTHON_VERSION >= 3.12" | bc -l) -eq 1 ]]; then
    log_with_timestamp "Python version $PYTHON_VERSION is not supported. Please use Python 3.11 or lower"
    exit 1
fi

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