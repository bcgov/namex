FROM python:3.12-slim

# Always ensure the latest security patches are applied
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

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
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    # poetry:
    POETRY_VERSION=1.8.3 \
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
    ca-certificates \
    openssl \
  && pip install --no-cache-dir setuptools \
  && pip install --no-cache-dir "poetry==${POETRY_VERSION}" \
  && poetry --version \
  && poetry config installer.max-workers 2 \
  && poetry config installer.parallel false \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Create user and workspace
WORKDIR /code
RUN groupadd -g "${GID}" -r web \
  && useradd -d '/code' -g web -l -r -u "${UID}" web \
  && chown web:web -R '/code' \
  && mkdir -p /var/cache/pypoetry \
  && chown web:web -R /var/cache/pypoetry

# Copy only requirements, to cache them in docker layer
COPY --chown=web:web ./poetry.lock ./pyproject.toml /code/

# Install dependencies with GitHub Actions optimizations
RUN --mount=type=cache,target="$POETRY_CACHE_DIR",uid=${UID},gid=${GID} \
  echo "Building for environment: ${APP_ENV:-development}" \
  && poetry version \
  && poetry config installer.max-workers 1 \
  && poetry install \
    $(if [ "$APP_ENV" = 'production' ] || [ -z "$APP_ENV" ]; then echo '--only main'; else echo '--with dev'; fi) \
    --no-interaction --no-ansi --verbose

# Switch to non-root user after installations
USER web

# Copy application code after dependencies are installed
COPY --chown=web:web ./namex /code/namex
COPY --chown=web:web ./README.md /code/
COPY --chown=web:web . /code

# Set secure permissions immediately after copying to remove write permissions
# Files: read-only (644), Directories: read+execute (755), wsgi.py: executable (755)
RUN find /code -type f -exec chmod 644 {} \; \
    && find /code -type d -exec chmod 755 {} \; \
    && chmod 755 /code/wsgi.py

# Run the server
ENV PYTHONPATH=/code
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--config", "/code/gunicorn_config.py", "wsgi:app"]