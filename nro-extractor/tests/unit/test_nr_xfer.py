import json

from . import integration_fdw_namex


@integration_fdw_namex
def test_nr_exrtact_invalid_nr_format(client):

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "nameRequest": "NR 1234567"
    }
    url = '/api/v1/nro-extract/nro-requests'

    response = client.post(url, data=json.dumps(data), headers=headers)

    # assert response.content_type == mimetype
    assert response.json['message'] == 'NR not found, unable to complete extraction to new system'
    assert response.status_code == 404
