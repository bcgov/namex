from urllib.parse import unquote_plus

from flask import current_app, jsonify, make_response, request

"""
General API resource utils.
"""


def log_error(msg, err):
    return msg.format(err)


def handle_exception(err, msg, err_code):
    current_app.logger.error('Error: ' + repr(err))
    return make_response(jsonify(message=msg), err_code)


def get_query_param_str(param):
    """Get a string param value from a request object."""
    param_value = request.args.get(param, None)
    return unquote_plus(param_value).strip() if param_value and isinstance(param_value, str) else None


def clean_url_path_param(param):
    return unquote_plus(param.strip()) if param and isinstance(param, str) else None
