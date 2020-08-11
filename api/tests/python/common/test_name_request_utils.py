import pytest


@pytest.mark.skip
def pick_name_from_list(names, name):
    matches = [n for n in names if n.get('name') == name]
    if len(matches) == 0:
        return None
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise Exception('More than one match for a name!')


@pytest.mark.skip
def assert_name_has_name(name):
    """
    Just a util
    :param name:
    :return:
    """
    assert name is not None
    assert name.get('name') is not None


@pytest.mark.skip
def assert_name_has_id(name):
    """
    Just a util
    :param name:
    :return:
    """
    assert name.get('id') is not None


@pytest.mark.skip
def assert_field_is_mapped(req_obj, res_obj, prop_name):
    """
    Just a util
    :param req_obj:
    :param res_obj:
    :param prop_name:
    :return:
    """
    req_obj_val = req_obj.get(prop_name)
    res_obj_val = res_obj.get(prop_name)
    print('Response Field [' + prop_name + ': ' + str(res_obj_val) + '] equals Request Field [' + prop_name + ': ' + str(req_obj_val) + ']')
    assert res_obj_val == req_obj_val
    print('OK')
    print('...')


@pytest.mark.skip
def assert_field_is_gt(req_obj, res_obj, prop_name):
    """
    Just a util
    :param req_obj:
    :param res_obj:
    :param prop_name:
    :return:
    """
    req_obj_val = req_obj.get(prop_name)
    res_obj_val = res_obj.get(prop_name)
    print('Response Field [' + prop_name + ': ' + str(res_obj_val) + '] is greater than Request Field [' + prop_name + ': ' + str(req_obj_val) + ']')
    assert res_obj_val > req_obj_val
    print('OK')
    print('...')


@pytest.mark.skip
def assert_field_is_lt(req_obj, res_obj, prop_name):
    """
    Just a util
    :param req_obj:
    :param res_obj:
    :param prop_name:
    :return:
    """
    req_obj_val = req_obj.get(prop_name)
    res_obj_val = res_obj.get(prop_name)
    print('Response Field [' + prop_name + ': ' + str(res_obj_val) + '] is less than Request Field [' + prop_name + ': ' + str(req_obj_val) + ']')
    assert res_obj_val < req_obj_val
    print('OK')
    print('...')


@pytest.mark.skip
def assert_field_has_value(res_obj, prop_name, prop_val):
    """
    Just a util
    :param res_obj:
    :param prop_name:
    :param prop_val:
    :return:
    """
    res_obj_val = res_obj.get(prop_name)
    print('Response Field [' + prop_name + ': ' + str(res_obj_val) + '] is equal to "' + str(prop_val) + '"')
    assert res_obj_val == prop_val
    print('OK')
    print('...')
