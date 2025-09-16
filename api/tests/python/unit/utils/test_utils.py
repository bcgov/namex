"""
Test suite for the utils.
"""

import pytest
from flask import Request
from werkzeug.test import EnvironBuilder

from namex.constants import ValidSources
from namex.models import Applicant, State
from namex.models import Request as RequestDAO


@pytest.mark.parametrize(
    'test_scenario,has_nr_num,has_temp_num,has_email,has_phone,header_has_nr,header_has_temp,header_has_email,header_has_phone,expected',
    [
        ('valid_nr', True, False, True, True, True, False, True, True, True),
        ('valid_temp_nr', False, True, True, True, False, True, True, True, True),
        ('no_nr', True, True, True, True, False, False, True, True, False),
        ('valid_nr_skip_nrl', True, True, True, True, True, True, True, True, True),
        ('valid_nr_only_email', True, True, True, True, True, True, True, False, True),
        ('valid_nr_only_phone', True, True, True, True, True, True, False, True, True),
        ('valid_nr_no_phone_no_email', True, True, True, True, True, True, False, False, False),
    ],
)
def test_full_access_to_name_request(
    test_scenario,
    has_nr_num,
    has_temp_num,
    has_email,
    has_phone,
    header_has_nr,
    header_has_temp,
    header_has_email,
    header_has_phone,
    expected,
    test_data_factory,
):
    """Assure that this contains the headers required to fully access an NR."""
    from namex.utils.auth import full_access_to_name_request

    # Generate unique data for this test run
    unique_nr_num = test_data_factory.generate_unique_nr_num() if has_nr_num else None
    unique_temp_num = f'NR L{test_data_factory.generate_unique_id()[:6]}' if has_temp_num else None
    unique_email = f'test{test_data_factory.generate_unique_id()}@example.com' if has_email else None
    unique_phone = f'250{test_data_factory.generate_unique_id()[:7]}' if has_phone else None

    # Setup NR
    nr = RequestDAO()
    nr.nrNum = unique_nr_num or unique_temp_num
    nr.stateCd = State.DRAFT
    nr._source = ValidSources.NAMEREQUEST.value
    applicant = Applicant()
    applicant.phoneNumber = unique_phone
    applicant.emailAddress = unique_email
    nr.applicants.append(applicant)
    nr.save_to_db()

    # Setup headers based on test scenario
    headers = {}
    if header_has_nr and unique_nr_num:
        headers['BCREG_NR'] = unique_nr_num
    if header_has_temp and unique_temp_num:
        headers['BCREG_NRL'] = unique_temp_num
    if header_has_email and unique_email:
        headers['BCREG-User-Email'] = unique_email
    if header_has_phone and unique_phone:
        headers['BCREG-User-Phone'] = unique_phone

    builder = EnvironBuilder(method='POST', data={}, headers=headers)
    env = builder.get_environ()
    req = Request(env)

    assert expected == full_access_to_name_request(req)
