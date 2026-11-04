from solr_admin.models.virtual_word_condition import VirtualWordCondition
from solr_admin.views.virtual_word_condition_view import VirtualWordConditionView
from hamcrest import *


def test_column_labels(db):
    view = VirtualWordConditionView(VirtualWordCondition, db.session)

    assert_that(view.column_labels, equal_to({
        'cnd_id': 'cnd_id',
        'word_id': 'word_id',
        'rc_consenting_body': 'consenting body',
        'rc_words': 'word phrase',
        'rc_condition_text': 'condition text',
        'rc_instructions': 'instructions',
        'rc_allow_use': 'allow use',
        'rc_consent_required': 'consent required'
    }))
