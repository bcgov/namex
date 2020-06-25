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


# TODO: Move this out into some sort of dict utils!
def mergedicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(mergedicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])