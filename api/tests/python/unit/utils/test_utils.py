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
    """
test_name,
name_request_number,temp_request_number,user_email,user_phone,
header_name_request_number,header_temp_request_number,header_user_email,header_user_phone,
expected""",
    [
        (
            'valid_nr',  # test_name
            'NR 0000001',  # name_request_number
            None,  # temp_request_number
            'info@example.com',  # user_email
            '1231231234',  # user_phone
            'NR 0000001',  # header_name_request_number
            None,  # header_temp_request_number
            'info@example.com',  # header_user_email
            '1231231234',  # header_user_phone
            True,
        ),  # expected
        (
            'valid_temp_nr',
            None,
            'NR L000001',
            'info@example.com',
            '1231231234',
            None,
            'NR L000001',
            'info@example.com',
            '1231231234',
            True,
        ),
        (
            'no_nr',
            'NR 0000001',
            'NR L000001',
            'info@example.com',
            '1231231234',
            None,
            None,
            'info@example.com',
            '1231231234',
            False,
        ),
        (
            'valid_nr_skip_nrl',
            'NR 0000001',
            'NR L000001',
            'info@example.com',
            '1231231234',
            'NR 0000001',
            'NR L000001',
            'info@example.com',
            '1231231234',
            True,
        ),
        (
            'valid_nr_only_email',
            'NR 0000001',
            'NR L000001',
            'info@example.com',
            '1231231234',
            'NR 0000001',
            'NR L000001',
            'info@example.com',
            None,
            True,
        ),
        (
            'valid_nr_only_phone',
            'NR 0000001',
            'NR L000001',
            'info@example.com',
            '1231231234',
            'NR 0000001',
            'NR L000001',
            None,
            '1231231234',
            True,
        ),
        (
            'valid_nr_no_phone_no_email',
            'NR 0000001',
            'NR L000001',
            'info@example.com',
            '1231231234',
            'NR 0000001',
            'NR L000001',
            None,
            None,
            False,
        ),
    ],
)
def test_full_access_to_name_request(
    test_name,
    name_request_number,
    temp_request_number,
    user_email,
    user_phone,
    header_name_request_number,
    header_temp_request_number,
    header_user_email,
    header_user_phone,
    expected,
):
    """Assure that this contains the headers required to fully access an NR."""
    from namex.utils.auth import full_access_to_name_request

    # setup
    nr = RequestDAO()
    nr.nrNum = name_request_number or temp_request_number
    nr.stateCd = State.DRAFT
    nr._source = ValidSources.NAMEREQUEST.value
    applicant = Applicant()
    applicant.phoneNumber = user_phone
    applicant.emailAddress = user_email
    nr.applicants.append(applicant)
    nr.save_to_db()

    builder = EnvironBuilder(
        method='POST',
        data={},
        headers={
            'BCREG_NR': header_name_request_number,
            'BCREG_NRL': header_temp_request_number,
            'BCREG-User-Email': header_user_email,
            'BCREG-User-Phone': header_user_phone,
        },
    )
    env = builder.get_environ()
    req = Request(env)

    print(req)

    assert expected == full_access_to_name_request(req)
