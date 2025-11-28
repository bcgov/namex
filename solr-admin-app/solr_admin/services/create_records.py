from solr_admin.models.restricted_condition_tmp import RestrictedConditionTmp
from solr_admin.models.restricted_word_tmp import RestrictedWordTmp
from solr_admin.models.restricted_word_condition_tmp import RestrictedWordConditionTmp


def create_records(virtual_word_condition, session):
    session.begin_nested()
    condition = RestrictedConditionTmp(
        consenting_body=virtual_word_condition.rc_consenting_body,
        cnd_text=virtual_word_condition.rc_condition_text,
        instructions=virtual_word_condition.rc_instructions,
        allow_use='Y' if virtual_word_condition.rc_allow_use or virtual_word_condition.rc_allow_use is None else 'N',
        consent_required='Y' if virtual_word_condition.rc_consent_required else 'N'
    )
    session.add(condition)
    session.commit()

    if virtual_word_condition.rc_words is not None:
        for word in virtual_word_condition.rc_words.split(','):
            word = RestrictedWordTmp(word_phrase=word.strip())
            session.begin_nested()
            session.add(word)
            session.commit()
            session.add(RestrictedWordConditionTmp(cnd_id=condition.cnd_id, word_id=word.word_id))

    session.commit()
