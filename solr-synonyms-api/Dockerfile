FROM python:3.8-slim-buster

ARG VCS_REF="missing"
ARG BUILD_DATE="missing"

LABEL org.label-schema.vcs-ref=${VCS_REF} \
      org.label-schema.build-date=${BUILD_DATE}

WORKDIR /opt/app-root

COPY ./requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

USER 1001

ENV PYTHONPATH=/opt/app-root

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--config", "/opt/app-root/gunicorn_config.py", "wsgi:application"]
