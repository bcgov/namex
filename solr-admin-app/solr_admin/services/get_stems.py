import os
import json
from urllib import request


def get_stems(synonym_list):
    try:
        response = json.load(request.urlopen(get_stems_url(synonym_list)))
        stems = extract_stems(response)
        stems_without_duplicates = list(set(stems))
        stems_without_duplicates.sort()

        return ', '.join(stems_without_duplicates)

    except:
        return synonym_list


def extract_stems(response):
    snowball_filter_response_index = 0
    analysis_steps = response['analysis']['field_names']['name']['index']
    for step in analysis_steps:
        if step == 'org.apache.lucene.analysis.snowball.SnowballFilter':
            snowball_filter_response_index += 1
            break
        snowball_filter_response_index += 1
    snowball_filter_response = analysis_steps[snowball_filter_response_index]

    return [text['text'] for text in snowball_filter_response]


def get_stems_url(synonym_list):
    solr_url = os.getenv('SOLR_URL')
    solr_base_url = solr_url + '/solr/possible.conflicts/analysis/field?analysis.fieldvalue='
    query = solr_base_url + '{words}&analysis.fieldname=name&wt=json&indent=true'.format(words=synonym_list.strip()).replace(' ', '%20')

    return query