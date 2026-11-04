from hamcrest import *


def test_can_assert():
    assert_that(1+1, equal_to(2))
