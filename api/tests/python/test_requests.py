
def test_requests_post(client):
    rv = client.post('/')
    assert b'swaggerui' in rv.data