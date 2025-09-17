# Stage 1: Builder stage
FROM python:3.12-slim AS builder

ARG VCS_REF="missing"
ARG BUILD_DATE="missing"
ARG APP_ENV
ARG UID=1000
ARG GID=1000

ENV VCS_REF=${VCS_REF} \
    BUILD_DATE=${BUILD_DATE} \
    APP_ENV=${APP_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

LABEL org.label-schema.vcs-ref=${VCS_REF} \
    org.label-schema.build-date=${BUILD_DATE}

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# Install system dependencies and Poetry
RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libpq-dev \
  && pip install --no-cache-dir "poetry==${POETRY_VERSION}" \
  && poetry --version \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Create user and workspace
RUN groupadd -g "${GID}" -r web \
  && useradd -d '/code' -g web -l -r -u "${UID}" web \
  && chown web:web /code \
  && mkdir -p /var/cache/pypoetry \
  && chown web:web /var/cache/pypoetry

# Copy only dependency files for better caching
COPY --chown=web:web pyproject.toml poetry.lock ./

# Install dependencies with optimized caching
RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
  poetry install \
  $(if [ "$APP_ENV" = 'production' ]; then echo '--only main'; else echo ''; fi) \
  --no-interaction --no-ansi

# clean up build tools after packages are installed
RUN apt-get purge -y --auto-remove \
    curl \
    build-essential \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Stage 2: Production image
FROM python:3.12-slim AS production

ARG UID=1000
ARG GID=1000

ENV PORT=8080 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code

# Install runtime dependencies only
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq5 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Create runtime user
RUN groupadd -g "${GID}" -r web \
  && useradd -d '/code' -g web -l -r -u "${UID}" web \
  && chown web:web /code

# Copy installed packages from builder
COPY --from=builder --chown=web:web /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder --chown=web:web /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=web:web . .

# Set secure permissions only on necessary files
RUN chmod 755 /code/wsgi.py /code/update_db.sh 2>/dev/null || true

USER web

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--config", "/code/gunicorn_config.py", "wsgi:app"]