import requests
import requests
from flask import current_app
from namex.utils.auth import get_client_credentials


class SolrClientException(Exception):
    def __init__(self, wrapped_err=None, body=None, message='Solr client exception', status_code=500):
        self.body = body
        self.err = wrapped_err
        if wrapped_err:
            self.message = '{msg}\r\n\r\n{desc}'.format(msg=message, desc=str(wrapped_err))
        else:
            self.message = message
        self.status_code = getattr(wrapped_err, 'status', status_code)
        super().__init__(self.message)

class SolrClientError(SolrClientException):
    def __init__(self, wrapped_err=None, body=None, message='Solr client error', status_code=400):
        super().__init__(wrapped_err=wrapped_err, body=body, message=message, status_code=status_code)

class SolrClient:
    @staticmethod
    def get_solr_api_url():
        return current_app.config.get('SOLR_API_URL')

    @staticmethod
    def _get_bearer_token():
        auth_url = current_app.config.get('SOLR_SVC_AUTH_URL', '')
        client_id = current_app.config.get('SOLR_API_SERVICE_ACCOUNT_CLIENT_ID', '')
        client_secret = current_app.config.get('SOLR_API_SERVICE_ACCOUNT_CLIENT_SECRET', '')

        authenticated, token = get_client_credentials(auth_url, client_id, client_secret)
        if not authenticated:
            raise SolrClientError('Client credentials request failed.')
        return token


    @staticmethod
    def search_nrs(query_value, start=0, rows=10):
        """
        Search NRs in Solr.
        :param query_value: value could be either NR name or NR number
        :param start: pagination start
        :param rows: number of rows to return
        """
        api_url = f'{SolrClient.get_solr_api_url()}/search/nrs'
        try:
            payload = {
                'query': {'value': query_value},  # value could be either NR name or NR number
                'start': start,
                'rows': rows
            }
            token = SolrClient._get_bearer_token()
            headers = {'Authorization': f'Bearer {token}'}
            resp = requests.post(api_url, json=payload, headers=headers)
            if resp.status_code != 200:
                raise SolrClientException(message=f'Solr search failed: {resp.text}', status_code=resp.status_code)
            return resp.json()
        except Exception as err:
            raise SolrClientException(wrapped_err=err)


    @classmethod
    def get_possible_conflicts(cls, name, start=0, rows=100):
        request_json = {
            'query': { 'value': name },
            'start': start,
            'rows': rows
        }

        token = SolrClient._get_bearer_token()
        resp = requests.post(
            url=f'{SolrClient.get_solr_api_url()}/search/possible-conflict-names',
            json=request_json,
            headers={'Authorization': f'Bearer {token}'}
        )
        if resp.status_code != 200:
            raise SolrClientException(message=f'Solr search failed: {resp.text}', status_code=resp.status_code)

        data = resp.json()
        seen = set()
        exact_matches = []
        similar_matches = []

        for r in data.get('searchResults', {}).get('results', []):
            n = r.get('name')
            if n in seen:
                continue
            seen.add(n)

            if n == name:
                r['type'] = 'exact'
                exact_matches.append(r)
            else:
                r['type'] = 'similar'
                similar_matches.append(r)

        return {
            'names': similar_matches,
            'exactNames': exact_matches
        }, '', None
