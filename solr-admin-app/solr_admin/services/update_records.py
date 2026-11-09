#import time
from solr_admin.models import db
from solr_admin.models.restricted_condition_tmp import RestrictedConditionTmp
from solr_admin.models.restricted_word_tmp import RestrictedWordTmp
from solr_admin.models.restricted_word_condition_tmp import RestrictedWordConditionTmp
from solr_admin.models.virtual_word_condition import VirtualWordCondition
from solr_admin.services.create_records import create_records

#@timeout(60)
def update_records(session):
    session.query(RestrictedWordConditionTmp).delete()
    session.query(RestrictedConditionTmp).delete()
    session.query(RestrictedWordTmp).delete()

    result = session.query(VirtualWordCondition).all()
    for row in result:
        create_records(row, session)

    session.commit()

    session.execute(db.text("DELETE FROM restricted_word_condition"))
    session.execute(db.text("INSERT INTO restricted_word_condition SELECT * FROM restricted_word_condition_tmp"))

    session.execute(db.text("DELETE FROM restricted_condition"))
    session.execute(db.text("INSERT INTO restricted_condition SELECT * FROM restricted_condition_tmp"))

    session.execute(db.text("DELETE FROM restricted_word"))
    session.execute(db.text("INSERT INTO restricted_word SELECT * FROM restricted_word_tmp"))

    session.commit()