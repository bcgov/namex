from flask import current_app, request, jsonify
from urllib.parse import unquote_plus
from functools import wraps
import asyncio

"""
General API resource utils.
"""


def log_error(msg, err):
    return msg.format(err)


def handle_exception(err, msg, err_code):
    current_app.logger.debug('Error: ' + repr(err))
    return jsonify(message=msg), err_code


def get_query_param_str(param):
    param_value = request.args.get(param)
    return unquote_plus(param_value).strip() if param_value and isinstance(param_value, str) else None


def clean_url_path_param(param):
    return unquote_plus(param.strip()) if param and isinstance(param, str) else None


def async_action(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped