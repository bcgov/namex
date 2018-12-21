import pytest
from namex.services.nro import utils


# testdata pattern is ({username}, {expected return value})
testdata = [
    ('idir/examiner', 'examine'),
    ('idir/', ''),
    ('github/examiner', 'examine'),
    ('/examiner', 'examine'),
    ('examiner', 'examine'),
    ('goofygoober', 'goofygo'),
    ('', '')
]


@pytest.mark.parametrize("username,expected", testdata)
def test_nro_examiner_name(username, expected):
    en = utils.nro_examiner_name(username)
    assert expected == en


compress_name_test_data = [
    ('the Waffle the Mania the', 'WAFFLEMANIATHE'),
    ('the Waffle 123 the Mania the', 'WAFFLEONETWOTHREEMANIATHE'),
    ('the Waffle !@$%^*()_+{}:"?><,./;[]\| the Mania the', 'WAFFLEMANIATHE'),
    ('the Waffle #$ the Mania the', 'WAFFLENUMBERMANIATHE'),
    ('the Waffle & the Mania the', 'WAFFLEANDMANIATHE'),
    ('BRITISHCOLUMBIA the Waffle the Mania BRITISHCOLUMBIA the', 'BCWAFFLEMANIABRITISHCOLUMBIATH')
]


@pytest.mark.parametrize("original_name,expected", compress_name_test_data)
def test_nro_generate_compressed_name(original_name, expected):
    result_name = utils.generate_compressed_name(original_name)
    assert expected == result_name

