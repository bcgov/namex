import pytest
from flask import request
from namex.constants import request_type_mapping


@pytest.mark.skip
def test_request_type_mapping(request_type_code):
    output = [item for item in request_type_mapping
              if item[0] == request_type_code]

    request._entity_type_cd = output[0][1]
    request._request_action_cd = output[0][2]


def test_request_type_mappings():
    types = ['CR', 'CCR', 'CT']

    for code in types:
        test_request_type_mapping(code)