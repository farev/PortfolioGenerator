#!/bin/bash

# Add timestamp to logs
log_with_timestamp() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log_with_timestamp "START: startup.sh execution"

# Create directories
log_with_timestamp "Creating directories..."
mkdir -p /home/site/wwwroot/.python_packages
mkdir -p /home/LogFiles/python

# Print debug info pre-installation
log_with_timestamp "Python version:"
python --version
log_with_timestamp "Current PYTHONPATH:"
echo $PYTHONPATH

# Install pip and upgrade it
log_with_timestamp "Upgrading pip..."
python -m ensurepip
python -m pip install --upgrade pip

# Install dependencies with pre-built wheels
log_with_timestamp "Installing dependencies..."
python -m pip install --target=/home/site/wwwroot/.python_packages -r /home/site/wwwroot/requirements.txt --only-binary :all: --prefer-binary

# Add the custom package directory to PYTHONPATH
export PYTHONPATH=/home/site/wwwroot/.python_packages:$PYTHONPATH
log_with_timestamp "Updated PYTHONPATH: $PYTHONPATH"

# List installed packages
log_with_timestamp "Installed packages:"
pip list

# Verify FastAPI installation
log_with_timestamp "Verifying FastAPI installation..."
python -c "import sys; print('Python path:', sys.path); import fastapi; print('FastAPI version:', fastapi.__version__)" || log_with_timestamp "FastAPI import failed"

# Start the application
log_with_timestamp "Starting application with Gunicorn..."
cd /home/site/wwwroot
PYTHONPATH=$PYTHONPATH gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 2 --log-level debug app:app 2>&1 | while read line; do log_with_timestamp "$line"; done 