import os

workers = int(os.environ.get("GUNICORN_PROCESSES", "1"))  # pylint: disable=invalid-name
threads = int(os.environ.get("GUNICORN_THREADS", "8"))  # pylint: disable=invalid-name
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "0"))  # pylint: disable=invalid-name


forwarded_allow_ips = "*"
secure_scheme_headers = {"X-Forwarded-Proto": "https"}
