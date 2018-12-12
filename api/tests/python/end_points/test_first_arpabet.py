from hamcrest import *
from namex.resources.phonetic import first_arpabet


def test_eek():
    assert_that(first_arpabet('LEAK'), equal_to('IY1'))


def test_ikk():
    assert_that(first_arpabet('LEEK'), equal_to('IY1'))




