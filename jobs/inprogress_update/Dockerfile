# Stage 1: Build environment (with Poetry + dependencies installed)
FROM python:3.12-slim AS development_build

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

COPY --chown=web:web . /code

COPY --chown=web:web ./run.sh /code/run.sh
RUN chmod 755 /code/run.sh

# Install dependencies
RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
    echo "$APP_ENV" \
    && poetry config installer.max-workers 1 \
    && poetry version \
    && poetry run pip install -U pip \
    && poetry install \
        $(if [ -z "${APP_ENV}" ] || [ "$APP_ENV" = 'production' ]; then echo '--only main'; fi) \
        --no-interaction --no-ansi

# Run as non-root
USER web

# Stage 2: Production image (lighter)
FROM development_build AS production_build
COPY --chown=web:web . /code
RUN chmod -R 755 /code/run.sh

EXPOSE 8080

CMD [ "/bin/sh", "/code/run.sh" ]