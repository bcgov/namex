from namex.services.name_request.exceptions import InvalidInputError
from namex.services.name_request.utils import normalize_nr_num


def parse_nr_num(nr_num_str):
    nr_num = normalize_nr_num(nr_num_str) if nr_num_str else None
    if nr_num_str and not nr_num:
        raise InvalidInputError(message='Invalid NR number format provided')

    return nr_num
