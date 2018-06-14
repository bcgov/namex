

def test_readyz(client):
    print('got to readyz')
    url = '/readyz'
    response = client.get(url)
    assert response.status_code == 200

def test_healthz(client):
    url = '/healthz'
    response = client.get(url)
    assert response.status_code == 200
    assert response.json['message'] == 'api is healthy'

def test_not_authenticated(client):
    url = '/corporations/A0003650'

    response = client.get(url)

    assert response.status_code == 401


