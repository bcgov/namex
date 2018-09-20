from namex.analytics.restricted_words import RestrictedWords


def test_gets_restricted():
    resp = RestrictedWords().get_restricted_words_conditions('DR')
    empty_resp = RestrictedWords().get_restricted_words_conditions('kial')

    # check word info
    assert resp[0]['restricted_words_conditions'][0]['word_info']['phrase'] == 'DR'
    assert resp[0]['restricted_words_conditions'][0]['word_info']['id'] is not None

    # check condition info
    assert resp[0]['restricted_words_conditions'][0]['cnd_info'][0]['allow_use'] is not None
    assert resp[0]['restricted_words_conditions'][0]['cnd_info'][0]['consent_required'] is not None
    assert resp[0]['restricted_words_conditions'][0]['cnd_info'][0]['consenting_body'] is not None
    assert resp[0]['restricted_words_conditions'][0]['cnd_info'][0]['id'] is not None
    assert resp[0]['restricted_words_conditions'][0]['cnd_info'][0]['instructions'] is not None
    assert resp[0]['restricted_words_conditions'][0]['cnd_info'][0]['text'] is not None

    # check empty
    assert empty_resp[0]['restricted_words_conditions'] == []
