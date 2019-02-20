from hamcrest import *
from solr_admin.services.get_stems import get_stems, get_stems_url
from solr_admin.models.synonym import Synonym

def test_populates_synonym_stems(browser, base_url, db):

    results = db.session.query(Synonym).all()

    for synons in results:
        synons.stems_text = get_stems(synons.synonyms_text)

    db.session.commit()

    assert_that(len(results), not_none())