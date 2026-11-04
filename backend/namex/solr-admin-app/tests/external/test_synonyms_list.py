from hamcrest import *
from solr_admin.models.synonym import Synonym
from tests.external.pages.synonyms_list_page import SynonymsListPage


def test_synonyms_list(browser, base_url, db):
    db.session.add(Synonym(category='hello', synonyms_text='world'))
    db.session.commit()

    page = SynonymsListPage(browser, base_url)
    assert_that(page.list_size(), equal_to(1))

    assert_that(page.category_of_row(1).text, equal_to('hello'))
    assert_that(page.synonyms_text_of_row(1).text, equal_to('world'))
