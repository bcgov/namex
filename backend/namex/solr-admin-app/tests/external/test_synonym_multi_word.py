from hamcrest import *

from solr_admin.models.synonym import Synonym
from tests.external.pages.synonym_creation_page import SynonymCreationPage



def test_multi_word_synonyms(browser, base_url, db):
    page = SynonymCreationPage(browser, base_url)
    page.fill('category', 'anything')
    page.fill('synonyms_text', 'me, hello world, hello again, stop')
    page.fill('comment', 'anything')
    page.save()

    #result = db.session.query(Synonym).all()

    #assert_that(len(result), equal_to(1))
    #assert_that(result[0].stems_text, equal_to('construct, develop'))

    errMsg = page.getErrorCell()
    assert_that(errMsg, equal_to('×\nMulti-word synonyms text cannot be processed here, please contact application support. (hello again, hello world)'))



