from hamcrest import *
from solr_admin.models.restricted_condition import RestrictedCondition2


def test_id_auto_creation(db):
    db.session.add(RestrictedCondition2(cnd_text='one'))
    db.session.add(RestrictedCondition2(cnd_text='two'))
    db.session.commit()
    conditions = db.session.query(RestrictedCondition2).all()

    assert_that(len(conditions), equal_to(2))

    first = conditions[0]
    assert_that(first.cnd_id, equal_to(1))

    second = conditions[1]
    assert_that(second.cnd_id, equal_to(2))