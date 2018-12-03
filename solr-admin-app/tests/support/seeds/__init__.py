from solr_admin.models.synonym import Synonym
from solr_admin.models.restricted_condition import RestrictedCondition2
from solr_admin.models.restricted_word_table import RestrictedWordTable


def seed_synonym(db, category='any', text=''):
    db.session.add(Synonym(category=category, synonyms_text=text))
    db.session.commit()


def seed_condition(db, cnd_id, consenting_body):
    db.session.add(RestrictedCondition2(cnd_id=cnd_id, consenting_body=consenting_body))
    db.session.commit()


def seed_full_condition(db, cnd_id, cnd_text, allow_use, consent_required, consenting_body, instructions):
    db.session.add(RestrictedCondition2(cnd_id=cnd_id, cnd_text=cnd_text, allow_use=allow_use,
                                        consent_required=consent_required, consenting_body=consenting_body,
                                        instructions=instructions))
    db.session.commit()


def seed_word(db, word_id, cnd_id, word):
    db.session.add(RestrictedWordTable(word_id=word_id, cnd_id=cnd_id, word=word))
    db.session.commit()
