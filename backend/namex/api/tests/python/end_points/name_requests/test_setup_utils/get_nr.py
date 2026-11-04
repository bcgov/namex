from ...common.http import build_request_uri, build_test_query
from ...common.logging import log_request_path
from ..configuration import API_BASE_URI

# These utils are in progress...


def get_nr_request_uri(nr_num):
    # This is to get NR by NR Num
    request_uri = API_BASE_URI + nr_num
    test_params = [{}]
    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    return path


def get_existing_nr_request_uri(nr_num):
    # This is to use existing NR search
    request_uri = API_BASE_URI
    test_params = [{'nrNum': nr_num}]
    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    return path
