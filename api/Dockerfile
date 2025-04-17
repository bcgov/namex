# ─── 1. Base + static installs ────────────────────────────────────────────────
FROM python:3.12-slim AS development_build
USER root

ARG APP_ENV \
  # Needed for fixing permissions of files created by Docker:
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
  POETRY_VERSION=1.3.2 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# 1.1 Install OS deps + Poetry
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
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# 1.2 Create non‑root user
RUN groupadd -g "${GID}" -r web \
  && useradd -d '/code' -g web -l -r -u "${UID}" web \
  && chown web:web -R '/code'


# ─── 2. Copy static files + install deps ─────────────────────────────────────
COPY --chown=web:web \
     poetry.lock pyproject.toml \
     config.py gunicorn_config.py wsgi.py \
     /code/

RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
  echo "$APP_ENV" \
  && poetry version \
  # Install deps:
  && poetry run pip install -U pip setuptools \
  && poetry install \
    $(if [ -z ${APP_ENV+x} ] | [ "$APP_ENV" = 'production' ]; then echo '--only main'; fi) \
    --no-interaction --no-ansi


# ─── 3. Copy application code ────────────────────────────────────────────────
COPY --chown=web:web ./namex /code/namex
USER web


# ─── 4. Final production image ───────────────────────────────────────────────
FROM development_build AS production_build

# 4.1 Inject dynamic metadata
ARG VCS_REF="missing"
ARG BUILD_DATE="missing"
LABEL org.label-schema.vcs-ref=${VCS_REF} \
      org.label-schema.build-date=${BUILD_DATE}
ENV VCS_REF=${VCS_REF} \
    BUILD_DATE=${BUILD_DATE}

# 4.2 Runtime settings
ENV PYTHONPATH=/code
EXPOSE 8080
CMD gunicorn --bind 0.0.0.0:8080 --config /code/gunicorn_config.py wsgi:app
