# Use Python 3.12.3 slim image as the base
FROM python:3.12-slim

# Set environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE 1  # Prevents creation of .pyc files
ENV PYTHONUNBUFFERED 1        # Ensures output is not buffered

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose the port (if applicable)
# EXPOSE 5000  # Uncomment if this is a web app

# Define the default command to run the application
CMD ["python", "app.py"]
