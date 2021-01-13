import re
import inflect
from itertools import product

_parse_csv_line = lambda x: (x.split(','))


def flatten_tuple_results(results):
    # Convert tuple results to a list of of CSV strings
    result_arr = [item for sublist in results for item in sublist]
    result_arr = [x.strip() for x in result_arr]

    result_arr = [*map(_parse_csv_line, result_arr)]
    flattened_arr = [item for sublist in result_arr for item in sublist]
    return flattened_arr


def parse_dict_of_lists(results):
    """
    Lucas - Changed from:
    output = {}
    for item in results:
        output[item.key] = sorted(list(set(item.list)), key=len, reverse=True)
    return output
    """
    try:
        output = {}
        for item in results:
            # TODO: This has been adjusted to handle either a dict or an object
            if isinstance(item, dict):
                output[item['key']] = sorted(list(set(item['list'])), key=len, reverse=True)
            else:
                output[getattr(item, 'key')] = sorted(list(set(getattr(item, 'list'))), key=len, reverse=True)
        return output
    except Exception as err:
        raise err


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


def merge_dicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(merge_dicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


def remove_periods_designation(results):
    designation_list = []
    for item in results:
        text = re.sub(r'[\.]', '', item, 0, re.IGNORECASE)
        designation_list.append(item)
        if text != item:
            designation_list.append(text)

    return designation_list


def get_plural_singular_name(name):
    d = {}
    p = inflect.engine()
    for word in name.split():
        val = []
        singular = p.singular_noun(word)
        plural = p.plural_noun(word)
        if singular:
            val.append(singular.lower())
        if plural:
            val.append(plural.lower())
        val.append(word.lower())
        d[word] = (list(set(val)))

    name_list = []
    for combination in product(*d.values()):
        name_list.append(' '.join(combination))

    return name_list


def convert_to_ascii(value):
    try:
        return value.encode("ascii", "ignore").decode('ascii')
    except Exception as err:
        return value


# def remove_numbers_list(list_name):
#    return [name for name in list_name if not name.isdigit()]


# def remove_numbers_dict(d):
#    return {key: value for key, value in d.items() if not key.isdigit()}
