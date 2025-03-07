#!/bin/bash
echo "Starting custom startup script"

# Create a user-writable directory for packages
mkdir -p /home/site/wwwroot/.python_packages

# Install dependencies to a writable location
echo "Installing dependencies..."
python -m pip install --target=/home/site/wwwroot/.python_packages -r /home/site/wwwroot/requirements.txt

# Add the custom package directory to PYTHONPATH
export PYTHONPATH=/home/site/wwwroot/.python_packages:$PYTHONPATH

# Print Python version and path for debugging
echo "Python version:"
python --version
echo "Python path:"
python -c "import sys; print(sys.path)"
echo "Checking for fastapi:"
python -c "import sys; sys.path.insert(0, '/home/site/wwwroot/.python_packages'); import fastapi; print(f'FastAPI version: {fastapi.__version__}')" || echo "FastAPI not found"

# Start the application
echo "Starting application with Gunicorn..."
cd /home/site/wwwroot
PYTHONPATH=/home/site/wwwroot/.python_packages:$PYTHONPATH gunicorn --bind=0.0.0.0:8000 app:app 2>&1 | tee /home/LogFiles/python/gunicorn.log 