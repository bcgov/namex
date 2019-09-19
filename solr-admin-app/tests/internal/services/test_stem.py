import os

from hamcrest import *
from solr_admin.services.get_stems import get_stems, get_stems_url
from urllib import request


def test_solr_configuration():
    assert_that(os.getenv('SOLR_URL'), not_none())


def test_solr_available():
    solr_url = os.getenv('SOLR_URL')
    url = solr_url + '/solr/possible.conflicts/admin/ping'
    r = request.urlopen(url)

    assert r.code == 200


def test_explore_stem_url():
    solr_url = os.getenv('SOLR_URL')
    synonym_list = 'construction, constructing, development'
    url = get_stems_url(synonym_list)

    assert_that(url, equal_to(solr_url + '/solr/possible.conflicts/analysis/field?analysis.fieldvalue=construction,%20constructing,%20development&analysis.fieldname=name&wt=json&indent=true'))


def test_stem_several_worlds():
    synonym_list = 'construction, constructing, development'
    stems = get_stems(synonym_list)

    assert_that(stems, equal_to('construct, develop'))
