
import json
import requests

'''
SOLR_BASE_URL = 'https://namex-solr-dev.pathfinder.gov.bc.ca/solr/trademarks/update/json'
SOLR_BASE_URL = 'https://namex-solr-test.pathfinder.gov.bc.ca/solr/trademarks/update/json'
SOLR_BASE_URL = 'https://namex-solr.pathfinder.gov.bc.ca/solr/trademarks/update/json'
'''

SOLR_BASE_URL = 'http://localhost:8983/solr/trademarks/update/json'

# Set this if, for example, you load 250,000 docs and then someone restarts the pod. Otherwise it should be 0.
SKIPPER = 0

# Clear the core.
if SKIPPER == 0:
    requests.post(SOLR_BASE_URL, json=json.loads('{ "delete": {"query": "*:*"}, "commit": {} }'))

count = 0
with open('trademarks.json') as file:
    for line in file:
        count = count + 1
        if count < SKIPPER:
            continue

        response = requests.post(SOLR_BASE_URL + '/docs', json=json.loads(line))

        if response.status_code != 200:
            print('{} {}'.format(response.status_code, response.json()))
            print('{}'.format(json))

        # Reload the index every thousand documents.
        if count % 1000 == 0:
            requests.post(SOLR_BASE_URL, json=json.loads('{ "commit": {} }'))
            print(count)

requests.post(SOLR_BASE_URL, json=json.loads('{ "commit": {} }'))
print(count)
