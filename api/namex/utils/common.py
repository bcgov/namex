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
