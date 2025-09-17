# Stage 1: Build environment (with Poetry + dependencies installed)
FROM python:3.12.5-slim AS development_build

ARG VCS_REF="missing"
ARG BUILD_DATE="missing"

ENV VCS_REF=${VCS_REF}
ENV BUILD_DATE=${BUILD_DATE}
ENV PORT=8080

LABEL org.label-schema.vcs-ref=${VCS_REF} \
      org.label-schema.build-date=${BUILD_DATE} \
      vendor="BCROS"

USER root

ARG APP_ENV \
    UID=1000 \
    GID=1000

ENV APP_ENV=${APP_ENV} \
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
    POETRY_VERSION=2.1.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

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
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version \
  # Clean up apt cache
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /code

RUN groupadd -g "${GID}" -r web \
  && useradd -d '/code' -g web -l -r -u "${UID}" web \
  && chown web:web -R '/code'

# Copy dependency files first (better caching)
COPY --chown=web:web ./poetry.lock ./pyproject.toml /code/

# Copy app source
COPY --chown=web:web ./src /code/src
COPY --chown=web:web ./README.md /code

# Install dependencies
RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
  echo "$APP_ENV" \
  && poetry version \
  && poetry update \
  && poetry install \
    $(if [ -z ${APP_ENV+x} ] || [ "$APP_ENV" = 'production' ]; then echo '--only main'; fi) \
    --no-interaction --no-ansi

# Run as non-root
USER web

# Stage 2: Production image (lighter)
FROM python:3.12-slim

WORKDIR /code

COPY --from=development_build /code /code

EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:${PORT} --config /code/gunicorn_config.py wsgi:app
