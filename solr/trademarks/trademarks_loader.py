
import requests

'''
SOLR_URL = 'https://namex-solr-dev.pathfinder.gov.bc.ca/solr/trademarks/update/json'
SOLR_URL = 'https://namex-solr-test.pathfinder.gov.bc.ca/solr/trademarks/update/json'
SOLR_URL = 'https://namex-solr.pathfinder.gov.bc.ca/solr/trademarks/update/json'
'''

SOLR_URL = 'http://localhost:8983/solr/trademarks/update/json'

# Set this if, for example, you load 250,000 docs and then someone restarts the pod. Otherwise it should be 0.
SKIPPER = 0

# Clear the core.
if SKIPPER == 0:
    requests.post(SOLR_URL, data='{ "delete": {"query": "*:*"}, "commit": {} }')

count = 0
json = []
with open('trademarks.json') as file:
    for line in file:
        count = count + 1
        if count < SKIPPER:
            continue

        json.append('"add": { "doc": ' + line + '}')

        # Print the count every thousand documents.
        if count % 1000 == 0:
            print(count)

        # 20 (or thereabouts) in a batch is the sweet spot when running locally.
        if count % 20 != 0:
            continue

        response = requests.post(SOLR_URL, data='{' + ','.join(json) + '}')

        if response.status_code != 200:
            print('{}'.format(json))
            print('{} {}'.format(response.status_code, response.text))

        json = []

if json:
    response = requests.post(SOLR_URL, data='{' + ','.join(json) + '}')

    if response.status_code != 200:
        print('{}'.format(json))
        print('{} {}'.format(response.status_code, response.text))

requests.post(SOLR_URL, data='{ "commit": {} }')
print(count)
