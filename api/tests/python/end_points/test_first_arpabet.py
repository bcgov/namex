from hamcrest import *
from namex.resources.phonetic import first_arpabet


def test_return_as_is_when_not_a_word():
    assert_that(first_arpabet('VANSEA'), equal_to('VANSEA'))
    assert_that(first_arpabet('VENIZIA'), equal_to('VENIZIA'))


def test_leak():
    assert_that(first_arpabet('LEAK'), equal_to(['L IY1 K']))





