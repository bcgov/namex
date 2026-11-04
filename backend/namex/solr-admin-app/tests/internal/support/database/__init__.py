from solr_admin.models.synonym import Synonym
from solr_admin.models.restricted_condition import RestrictedCondition
from solr_admin.models.restricted_word import RestrictedWord
from solr_admin.models.restricted_word_condition import RestrictedWordCondition


def seed_synonym(db, category='any', text=''):
    db.session.add(Synonym(category=category, synonyms_text=text))
    db.session.commit()


def seed_condition(db, consenting_body, condition_text=None, instructions=None):
    condition = RestrictedCondition(consenting_body=consenting_body, cnd_text=condition_text, instructions=instructions)
    db.session.add(condition)
    db.session.commit()

    return condition.cnd_id


def seed_full_condition(db, cnd_id, cnd_text, allow_use, consent_required, consenting_body, instructions):
    db.session.add(RestrictedCondition(cnd_id=cnd_id, cnd_text=cnd_text, allow_use=allow_use,
                                       consent_required=consent_required, consenting_body=consenting_body,
                                       instructions=instructions))
    db.session.commit()


def seed_word(db, word):
    restricted_word = RestrictedWord(word_phrase=word)
    db.session.add(restricted_word)
    db.session.commit()

    return restricted_word.word_id


def seed_word_condition(db, cnd_id, word_id):
    db.session.add(RestrictedWordCondition(cnd_id=cnd_id, word_id=word_id))
    db.session.commit()


def seed_condition_and_words(db, consenting_body, words, condition_text=None, instructions=None):
    cnd_id = seed_condition(db, consenting_body=consenting_body, condition_text=condition_text, instructions=instructions )
    for word in words.split(','):
        word_id = seed_word(db, word=word.strip())
        seed_word_condition(db, cnd_id, word_id)


