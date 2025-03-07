#!/bin/bash
echo "Starting custom startup script"

# Create directories
mkdir -p /home/site/wwwroot/.python_packages
mkdir -p /home/LogFiles/python

# Install dependencies to a writable location
echo "Installing dependencies..."
python -m pip install --target=/home/site/wwwroot/.python_packages -r /home/site/wwwroot/requirements.txt

# Add the custom package directory to PYTHONPATH
export PYTHONPATH=/home/site/wwwroot/.python_packages:$PYTHONPATH

# Print debug info
echo "Python version:"
python --version
echo "Python path:"
echo $PYTHONPATH

# Start the application
echo "Starting application with Gunicorn..."
cd /home/site/wwwroot
PYTHONPATH=$PYTHONPATH gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 2 app:app 