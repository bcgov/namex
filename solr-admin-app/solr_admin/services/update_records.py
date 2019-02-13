from solr_admin.models.restricted_condition import RestrictedCondition
from solr_admin.models.restricted_word import RestrictedWord
from solr_admin.models.restricted_word_condition import RestrictedWordCondition
from solr_admin.models.virtual_word_condition import VirtualWordCondition
from solr_admin.services.create_records import create_records


def update_records(session):
    session.query(RestrictedWordCondition).delete()
    session.query(RestrictedCondition).delete()
    session.query(RestrictedWord).delete()

    result = session.query(VirtualWordCondition).all()
    for row in result:
        create_records(row, session)

    session.commit()
