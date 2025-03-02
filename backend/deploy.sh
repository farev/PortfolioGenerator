#!/bin/bash
echo "Starting deployment script..."

# Navigate to the deployment directory
cd /home/site/wwwroot
echo "Current directory: $(pwd)"

# Install Python dependencies
echo "Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Make startup script executable
echo "Making startup script executable..."
chmod +x startup.sh

echo "Deployment script completed." 