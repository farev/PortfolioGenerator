FROM python:3.10-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make sure the startup script is executable
RUN chmod +x startup.sh

# Set environment variables
ENV PORT=8000

# Run the startup script
CMD ["./startup.sh"] 