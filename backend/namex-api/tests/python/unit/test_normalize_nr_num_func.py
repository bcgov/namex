import re

from namex.services.name_request.utils import normalize_nr_num, nr_regex


def test_normalize_nr_num_pattern():
    # Test regex pattern
    test_nr_num = 'NR L005005'
    matches = re.findall(nr_regex, test_nr_num, flags=re.IGNORECASE)
    assert matches[0][1] == '005005'

    test_nr_num = 'NR 005005'
    matches = re.findall(nr_regex, test_nr_num, flags=re.IGNORECASE)
    assert matches[0][1] == '005005'

    test_nr_num = 'NR005005'
    matches = re.findall(nr_regex, test_nr_num, flags=re.IGNORECASE)
    assert matches[0][1] == '005005'

    test_nr_num = 'NR005'
    matches = re.findall(nr_regex, test_nr_num, flags=re.IGNORECASE)
    assert len(matches) == 0

    test_nr_num = '005005'
    matches = re.findall(nr_regex, test_nr_num, flags=re.IGNORECASE)
    assert matches[0][1] == '005005'

    test_nr_num = '005'
    matches = re.findall(nr_regex, test_nr_num, flags=re.IGNORECASE)
    assert len(matches) == 0


def test_normalize_nr_num_func():
    test_nr_num = 'NR L005005'
    result_str = normalize_nr_num(test_nr_num)
    assert result_str == 'NR L005005'

    test_nr_num = 'NR 005005'
    result_str = normalize_nr_num(test_nr_num)
    assert result_str == 'NR 005005'

    test_nr_num = 'nr l005005'
    result_str = normalize_nr_num(test_nr_num)
    assert result_str == 'NR L005005'

    test_nr_num = 'nr 005005'
    result_str = normalize_nr_num(test_nr_num)
    assert result_str == 'NR 005005'

    test_nr_num = 'NR005005'
    result_str = normalize_nr_num(test_nr_num)
    assert result_str == 'NR 005005'

    test_nr_num = 'NR005'
    result_str = normalize_nr_num(test_nr_num)
    assert result_str is None

    test_nr_num = '005005'
    result_str = normalize_nr_num(test_nr_num)
    assert result_str == 'NR 005005'

    test_nr_num = '005'
    result_str = normalize_nr_num(test_nr_num)
    assert result_str is None
