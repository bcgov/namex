# Use Python 3.12.3 slim image as the base
FROM python:3.12-slim

# Set environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies with no recommended packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential=12.9 \
        libpq-dev=13.4-1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user and set permissions
RUN useradd --create-home appuser
WORKDIR /home/appuser

# Copy only required files for dependencies
COPY pyproject.toml poetry.lock /home/appuser/

# Install dependencies using Poetry
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry install --no-root --no-dev

# Copy application source code selectively
COPY src /home/appuser/src
COPY app.py /home/appuser/

# Set appropriate permissions
RUN chown -R appuser:appuser /home/appuser

# Switch to the non-root user
USER appuser

# Define the default command to run the application
CMD ["poetry", "run", "python", "app.py"]
