from hamcrest import *
from solr_admin.models.synonym import Synonym


def test_id_auto_creation(db):
    db.session.add(Synonym(synonyms_text='one'))
    db.session.add(Synonym(synonyms_text='two'))
    db.session.commit()
    synonyms = db.session.query(Synonym).all()

    assert_that(len(synonyms), equal_to(2))

    first = synonyms[0]
    assert_that(first.id, equal_to(1))

    second = synonyms[1]
    assert_that(second.id, equal_to(2))

