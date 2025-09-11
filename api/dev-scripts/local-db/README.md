# NameX API - Docker Development Setup

This guide provides instructions for setting up the NameX API with PostgreSQL using Docker Compose for local development.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.12 with Poetry
- Git

## Quick Start

### 1. Start PostgreSQL Database

```bash
# From this directory (dev-scripts/local-db)
docker compose up -d

# Verify the database is running
docker compose ps
```

This will start a PostgreSQL 15 container with:
- **Container name**: `namex-postgres`
- **Database**: `namex`
- **Username**: `namex`
- **Password**: `postgres`
- **Port**: `54345` (mapped from container port 5432)

### 2. Configure Environment Variables

Create or update your `.env` file in the API root directory with the following database configuration:

```bash
# Database Configuration for Docker
DATABASE_USERNAME="posrgres"
DATABASE_PASSWORD="postgres"
DATABASE_NAME="namex"
DATABASE_HOST="localhost"
DATABASE_PORT="54345"
DATABASE_SCHEMA="namex"
DATABASE_OWNER="namex"

# Set to migration mode to initialize database schema
DEPLOYMENT_ENV=migration
```

**Important**: These values must match the Docker Compose configuration in this `docker-compose.yml` file.

### 3. Run Database Migrations

```bash
# From the API root directory (../../)
# Load environment variables and run migrations
set -a
source .env
set +a
poetry run flask db upgrade
poetry run flask db downgrade
```