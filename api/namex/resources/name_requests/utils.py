from flask import request, jsonify
from urllib.parse import unquote_plus


def log_error(msg, err):
    return msg.format(err)


def handle_exception(err, msg, err_code):
    log_error(msg + ' Error:{0}', err)
    return jsonify(message=msg), err_code


def get_query_param_str(param):
    param_value = request.args.get(param)
    return unquote_plus(param_value).strip() if param_value and isinstance(param_value, str) else None


def query_result_to_dict(result):
    """
    SQLAlchemy returns tuples, they need to be converted to dict so we can jsonify
    :return:
    """
    return dict(zip(result.keys(), result))


def query_results_to_dict(results):
    """
    SQLAlchemy returns tuples, they need to be converted to dict so we can jsonify
    :return:
    """
    return list(map(lambda result: query_result_to_dict(result), results))
