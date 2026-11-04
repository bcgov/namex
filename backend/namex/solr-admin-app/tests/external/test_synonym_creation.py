from hamcrest import *
from solr_admin.models.synonym import Synonym
from tests.external.pages.synonym_creation_page import SynonymCreationPage


def test_populates_synonym_stems(browser, base_url, db):
    page = SynonymCreationPage(browser, base_url)
    page.fill('category', 'anything')
    page.fill('synonyms_text', 'construction, constructing, development')
    page.fill('comment', 'anything')
    page.save()

    result = db.session.query(Synonym).all()

    assert_that(len(result), equal_to(1))
    assert_that(result[0].stems_text, equal_to('construct, develop'))
