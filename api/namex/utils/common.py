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
    # TODO: This is a temporary method to transform data from the synonyms api
    # I don't really like that we have to use this, but it's the quickest way to get things
    # running again after pulling out the synonyms service into a self-contained app
    output = {}
    for item in results:
        output[item.key] = item.list
    return output


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
        if singular is not False:
            val.extend([singular])
        val.extend([word.lower()])
        d[word] = (list(set(val)))

    name_list = []
    for combination in product(*d.values()):
        name_list.append(' '.join(combination))

    return name_list


#def remove_numbers_list(list_name):
#    return [name for name in list_name if not name.isdigit()]


#def remove_numbers_dict(d):
#    return {key: value for key, value in d.items() if not key.isdigit()}
