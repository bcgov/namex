import pytest
from namex.constants import EntityTypes, RequestAction, request_type_mapping
from tests.python.conftest import app


@pytest.mark.skip
def test_request_type_mapping(request_type_code):
    output = [item for item in request_type_mapping
              if item[0] == request_type_code]

    if request_type_code == 'CR':
        assert output[0][0] == 'CR'
        assert output[0][1] == EntityTypes.CORPORATION.value
        assert output[0][2] == RequestAction.NEW_AML.value
        assert output[0][3] is True
        assert output[1][0] == 'CR'
        assert output[1][1] == EntityTypes.CORPORATION.value
        assert output[1][2] == RequestAction.NEW.value
        assert output[2][0] == 'CR'
        assert output[2][1] == EntityTypes.CORPORATION.value
        assert output[2][2] == RequestAction.AML.value
    if request_type_code == 'CCR':
        assert output[0][0] == 'CCR'
        assert output[0][1] == EntityTypes.CORPORATION.value
        assert output[0][2] == RequestAction.CHG.value
        assert output[0][3] is True
        assert output[1][0] == 'CCR'
        assert output[1][1] == EntityTypes.CORPORATION.value
        assert output[1][2] == RequestAction.RESUBMIT.value
    if request_type_code == 'CT':
        assert output[0][0] == 'CT'
        assert output[0][1] == EntityTypes.CORPORATION.value
        assert output[0][2] == RequestAction.MVE.value
        assert output[0][3] is True
        assert output[1][0] == 'CT'
        assert output[1][1] == EntityTypes.CORPORATION.value
        assert output[1][2] == RequestAction.RESUBMIT.value


def test_request_type_mappings():
    types = ['CR', 'CCR', 'CT']
    for code in types:
        test_request_type_mapping(code)
