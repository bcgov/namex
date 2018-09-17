

def test_jobs(client):
    rv = client.get('/')
    assert b'Name Request API' in rv.data
