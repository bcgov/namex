import pytest
from nro import utils


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
