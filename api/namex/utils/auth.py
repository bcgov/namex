import requests


def cors_preflight(methods):
    def wrapper(f):

        def options(self,  *args, **kwargs):
            return {'Allow': 'GET'}, 200, \
                   {'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': methods,
                    'Access-Control-Allow-Headers': 'Authorization, Content-Type'}

        setattr(f, 'options', options)
        return f
    return wrapper


MSG_CLIENT_CREDENTIALS_REQ_FAILED = 'Client credentials request failed'


def get_client_credentials(auth_url, client_id, secret):
    auth = requests.post(
        auth_url,
        auth=(client_id, secret),
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': secret
        }
    )

    # Return the auth response if an error occurs
    if auth.status_code != 200:
        # TODO: This is mocked out
        # return True, 'asdf-asdf-asdf-adsf'
        return False, auth.json()

    token = dict(auth.json())['access_token']
    return True, token


