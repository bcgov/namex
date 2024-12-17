# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_HOME="/usr/local"

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Poetry
RUN python3 -m ensurepip --upgrade && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version

WORKDIR /app

# Copy dependency files and install dependencies
COPY --chown=appuser:appuser pyproject.toml poetry.lock /app/
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the application source code
COPY --chown=appuser:appuser src /app/src

# OpenShift will assign a random UID
USER 1001

# Default command
CMD ["python", "src/app.py"]
