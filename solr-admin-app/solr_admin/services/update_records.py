from solr_admin.models.restricted_condition_tmp import RestrictedConditionTmp
from solr_admin.models.restricted_word_tmp import RestrictedWordTmp
from solr_admin.models.restricted_word_condition_tmp import RestrictedWordConditionTmp
from solr_admin.models.virtual_word_condition import VirtualWordCondition
from solr_admin.services.create_records import create_records

@timeout(60)
def update_records(session):
    session.query(RestrictedWordConditionTmp).delete()
    session.query(RestrictedConditionTmp).delete()
    session.query(RestrictedWordTmp).delete()

    result = session.query(VirtualWordCondition).all()
    for row in result:
        create_records(row, session)

    session.commit()

    session.execute(db.text("DROP TABLE restricted_word_condition"))
    session.execute(db.text("CREATE TABLE restricted_word_condition AS SELECT * from restricted_word_condition_tmp"))

    session.execute(db.text("DROP TABLE restricted_condition"))
    session.execute(db.text("CREATE TABLE restricted_condition AS SELECT * from restricted_condition_tmp"))
    
    session.execute(db.text("DROP TABLE restricted_word"))
    session.execute(db.text("CREATE TABLE restricted_word AS SELECT * from restricted_word_tmp"))

    session.commit()