import re
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


nr_regex = r'^(NR\ ?L{0,1}?)?([\d]{6,8})$'


def normalize_nr_num(nr_num_str):
    matches = re.findall(nr_regex, nr_num_str, flags=re.IGNORECASE)
    # If there's a match and the match has a second capturing group (valid NR digits) then proceed
    if len(matches) == 1 and matches[0][1]:
        # Get the first capturing group if it exists, convert to upper case, and remove any spaces
        nr_type = str(matches[0][0]).upper().replace(' ', '') if matches[0][0] else 'NR'  # Default to NR if not supplied
        # Grab the NR digits from the second capturing group
        digits = matches[0][1]

        if nr_type == 'NR':
            return 'NR ' + digits
        if nr_type == 'NRL':
            return 'NR L' + digits

    return None
