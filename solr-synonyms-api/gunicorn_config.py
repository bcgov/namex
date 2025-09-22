"""Gunicorn config."""
import os

workers = int(os.environ.get("GUNICORN_PROCESSES", "1"))
threads = int(os.environ.get("GUNICORN_THREADS", "3"))
# 0 for unlimited -- 8190 is the highest set value
limit_request_line = int(os.environ.get("GUNICORN_MAX_REQUEST_LINE", "0"))

forwarded_allow_ips = "*"
secure_scheme_headers = {"X-Forwarded-Proto": "https"}
