# syntax=docker/dockerfile:1
# platform=linux/amd64
FROM python:3.12.2-slim

ARG VCS_REF="missing"
ARG BUILD_DATE="missing"
ARG APP_ENV
ARG UID=1000
ARG GID=1000

ENV VCS_REF=${VCS_REF} \
    BUILD_DATE=${BUILD_DATE} \
    APP_ENV=${APP_ENV} \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    # poetry:
    POETRY_VERSION=1.3.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    # app:
    PYTHONPATH=/code

LABEL org.label-schema.vcs-ref=${VCS_REF} \
    org.label-schema.build-date=${BUILD_DATE}

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# Install system dependencies and Poetry in a single layer
RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    brotli \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wait-for-it \
  && curl -sSL 'https://install.python-poetry.org' | POETRY_VERSION=${POETRY_VERSION} python - \
  && poetry --version \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Create user and workspace
WORKDIR /code
RUN groupadd -g "${GID}" -r web \
  && useradd -d '/code' -g web -l -r -u "${UID}" web \
  && chown web:web -R '/code'

# Switch to non-root user early
USER web

# Copy only requirements, to cache them in docker layer
COPY --chown=web:web ./poetry.lock ./pyproject.toml /code/

# Project initialization - install dependencies first for better caching
RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
  echo "$APP_ENV" \
  && poetry version \
  # Install deps:
  && poetry run pip install -U pip \
  && poetry install \
    $(if [ -z ${APP_ENV+x} ] || [ "$APP_ENV" = 'production' ]; then echo '--only main'; fi) \
    --no-interaction --no-ansi

# Copy application code after dependencies are installed
COPY --chown=web:web ./namex /code/namex
COPY --chown=web:web ./README.md /code/
COPY --chown=web:web . /code

# Run the server
ENV PYTHONPATH=/code
EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:8080 --config /code/gunicorn_config.py wsgi:app
