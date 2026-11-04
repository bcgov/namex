from namex.models.restricted_words import RestrictedWords


def test_get_restricted_short():
    resp = RestrictedWords().get_restricted_words_conditions('DR')
    empty_resp = RestrictedWords().get_restricted_words_conditions('')

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


def test_get_restricted_long(db):
    # test strip_content
    content = RestrictedWords().strip_content('+DR. -royal @"bc" *bc??royalre* nd')
    assert '+' not in content
    assert '-' not in content
    assert '@' not in content
    assert '"' not in content
    assert '*' not in content
    assert '?' not in content
    assert 'r' not in content  # uppercase check
    assert content == ' DR ROYAL BC BCROYALRE ND '

    # test find_restricted_words
    restricted_info = RestrictedWords.find_restricted_words(content)
    returned_words = []
    for obj in restricted_info:
        assert 'phrase' in obj
        assert 'id' in obj

        returned_words.append(obj['phrase'])

    expected_words = ['BC', 'DR', 'ROYAL', 'ROYAL BC', 'ND']
    assert set(returned_words).issubset(expected_words)
    assert set(expected_words).issubset(returned_words)

    # test find_cnd_info
    for word in restricted_info:
        cnd_info = RestrictedWords.find_cnd_info(word['id'])
        for cnd in cnd_info:
            assert 'allow_use' in cnd
            assert 'consent_required' in cnd
            assert 'consenting_body' in cnd
            assert 'id' in cnd
            assert 'instructions' in cnd
            assert 'text' in cnd
