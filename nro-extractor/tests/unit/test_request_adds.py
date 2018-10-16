import pytest


nr_applicants_test_data = [
    ({'lastName': 'last_name',
      'firstName': 'first_name',
      'middleName': 'middle_name',
      'phoneNumber': '111.111.1111',
      'faxNumber': '111.111.1111',
      'emailAddress': 'email_address',
      'contact' : 'contact',
      'clientFirstName': 'first_name',
      'clientLastName': 'last_name',
      'declineNotificationInd': 'Y',
      'addrLine1': 'addr_line_1',
      'addrLine2': 'addr_line_2',
      'addrLine3' : 'addr_line_3',
      'city': 'city',
      'postalCd': 'postal_cd',
      'stateProvinceCd': 'BC',
      'countryTypeCd': 'CA'
      },
     {'last_name': 'new_last_name',
      'first_name': 'new_first_name',
      'middle_name': 'new_middle_name',
      'phone_number': '222.222.2222',
      'fax_number': '222.222.2222',
      'email_address': 'tom@example.com',
      'contact' : None,
      'client_first_name': 'cl_first_name',
      'client_last_name': 'cl_last_name',
      'decline_notification_ind': 'N',
      'addr_line_1': '1234 Alder',
      'addr_line_2': 'Suite 100',
      'addr_line_3' : None,
      'city': 'Victoria',
      'postal_cd': 'X0X0X0',
      'state_province_cd': 'AB',
      'country_type_cd': 'AG'
      }
    )
]


@pytest.mark.parametrize("applicant1 ,applicant2", nr_applicants_test_data)
def test_request_add_applicant_existing(app, request, session, applicant1, applicant2):

    # imports for just this test
    from namex.models import Request, Applicant, User
    from api.endpoints.requests import add_applicant

    # SETUP
    # create an NR and add an applicant
    nr = Request()
    nr.activeUser = User('idir/bob', 'bob', 'last', 'idir', 'localhost')
    nr.applicants.append(Applicant(**applicant1))

    session.add(nr)
    session.commit()

    # Test
    # Call add_applicant and then assert the new NR applicant matches our data

    add_applicant(nr, applicant2, update=True)

    session.add(nr)
    session.commit()

    appl = nr.applicants.one_or_none()

    nra = dict_to_json_keys(applicant2)
    a = appl.as_dict()
    if a.get('partyId'): a.pop('partyId')

    # check entire dict
    assert nra == a


# utility routine
def dict_to_json_keys(pydict: dict) -> dict:
    """this converts a dict using the python coding style to a dict
    where the keys are in JSON format style
    :pydict dict keys are strings in python style format
    :returns dict
    """
    d = {}
    for key in pydict.keys():
        new_key = key.title().replace('_', '')
        new_key = new_key[:1].lower() + new_key[1:]
        d[new_key] = pydict[key]
    return d
