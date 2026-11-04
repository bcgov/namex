def test_root_page_has_swaggerui(client):
    rv = client.get('/')
    assert b'Name Request API' in rv.data
