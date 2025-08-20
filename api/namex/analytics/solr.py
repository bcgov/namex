import re

import requests
from flask import current_app


class SolrQueries:

    @classmethod
    def get_possible_conflicts(cls, name, start=0, rows=100):
        request_json = {
            'query': { 'value': name },
            'start': start,
            'rows': rows
        }

        resp = requests.post(
            url=f'{current_app.config.get('SOLR_API_URL')}/search/possible-conflict-names',
            json=request_json,
            headers={'Authorization': f'Bearer {cls._get_solr_api_bearer_token()}'}
        )
        if resp.status_code != 200:
            current_app.logger.error(
                f'Failed calling solr-search-api. Status={resp.status_code}, body={resp.text}'
            )
            return None, 'Internal server error', 500

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


    @classmethod
    def get_name_requests(cls, nr_num=None, name=None, start=0, rows=10):
        if not nr_num and not name:
            return {'response': {'numFound': 0, 'start': start, 'rows': rows}, 'names': []}

        def fetch(query_value):
            resp = requests.post(
                f'{current_app.config.get('SOLR_API_URL')}/search/nrs',
                json={'query': {'value': query_value}, 'start': start, 'rows': rows},
                headers={'Authorization': f'Bearer {cls._get_solr_api_bearer_token()}'}
            )
            data = resp.json() or {}
            sr = data.get('searchResults', {})
            qi = sr.get('queryInfo', {}) or {}
            return {
                'response': {
                    'numFound': sr.get('totalResults', 0),
                    'start': qi.get('start', start),
                    'rows': qi.get('rows', rows),
                },
                'names': sr.get('results', [])
            }

        combined = {'response': {'numFound': 0, 'start': start, 'rows': rows}, 'names': []}
        seen = set()

        for q in [nr_num, name]:
            if not q:
                continue
            part = fetch(q)
            combined['response']['numFound'] += part['response']['numFound']
            for item in part['names']:
                key = item.get('nr_num')
                if key and key not in seen:
                    seen.add(key)
                    combined['names'].append(item)

        return combined


    @classmethod
    def extract_nr_number_and_name(cls, value: str):
        """
        Parse a mixed query into (nr_number, name_value).

        Examples:
        - None / ""                   -> (None, "")
        - "NR 1234567"                -> ("1234567", "")
        - "HNR239 HOLDINGS"           -> (None, "HNR239 HOLDINGS")
        - "NR 955 HNR239 HOLDINGS"    -> ("955", "HNR239 HOLDINGS")
        - "HNR239 HOLDINGS NR 955"    -> ("955", "HNR239 HOLDINGS")
        - "HNR239 NR 955 HOLDINGS"    -> ("955", "HNR239 HOLDINGS")
        """
        if not value:
            return None, None

        q = value.strip()

        # 1) Prefer explicit NR token
        m = re.compile(r'(?:^|\s)(NR\s*\d+)(?:\s|$)', re.IGNORECASE).search(q)
        if m:
            nr_token = m.group(1)
            nr_number = re.sub(r'[^0-9]', '', nr_token)
            # remove the matched token from the name part
            name_value = (q[:m.start(1)] + q[m.end(1):]).strip()
            # collapse multiple spaces
            name_value = re.sub(r'\s+', ' ', name_value)
            return (nr_number or None), name_value

        # 2) Fallback: a bare digits token (e.g., "955")
        m = re.compile(r'(?:^|\s)(\d+)(?:\s|$)').search(q)
        if m:
            nr_number = m.group(1).strip()
            name_value = (q[:m.start(1)] + q[m.end(1):]).strip()
            name_value = re.sub(r'\s+', ' ', name_value)
            return (nr_number or None), name_value

        # 3) No NR found -> all name
        return None, re.sub(r'\s+', ' ', q)

    @classmethod
    def _get_solr_api_bearer_token(cls) -> str:
        auth_url = current_app.config.get('ENTITY_SVC_AUTH_URL', None)
        client_id = current_app.config.get('SOLR_API_SERVICE_ACCOUNT_CLIENT_ID', None)
        client_secret = current_app.config.get('SOLR_API_SERVICE_ACCOUNT_CLIENT_SECRET', None)

        resp = requests.post(
            auth_url,
            auth=(client_id, client_secret),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret
            }
        )

        if resp.status_code != 200:
            return None
        return resp.json().get('access_token')
