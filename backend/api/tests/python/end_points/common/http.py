from urllib.parse import quote_plus


def get_test_headers():
    return {'content-type': 'application/json'}


def build_test_query(test_params):
    query = ''

    for entry in test_params:
        query += '&'.join('{!s}={}'.format(k, quote_plus(v)) for (k, v) in entry.items())

    return query


def build_request_uri(request_uri, query):
    return request_uri + '?' + query if len(query) > 0 else request_uri


def setup_test_token(jwt, claims, token_header):
    token = jwt.create_jwt(claims, token_header)
    return token, {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
