_parse_csv_line = lambda x: (x.split(','))


def flatten_tuple_results(results):
    # Convert tuple results to a list of of CSV strings
    result_arr = [item for sublist in results for item in sublist]
    result_arr = [x.strip() for x in result_arr]

    result_arr = [*map(_parse_csv_line, result_arr)]
    flattened_arr = [item for sublist in result_arr for item in sublist]
    return flattened_arr
