draft_data = {
    'applicants': [
        {
            'addrLine1': '1796 KINGS RD',
            'addrLine2': '',
            'city': 'VICTORIA',
            'clientFirstName': '',
            'clientLastName': '',
            'contact': '',
            'countryTypeCd': 'CA',
            'emailAddress': 'example@example.com',
            'faxNumber': '',
            'firstName': 'BOB',
            'lastName': 'JOHNSON',
            'middleName': '',
            'phoneNumber': '2505320083',
            'postalCd': 'V8R 2P1',
            'stateProvinceCd': 'BC',
        }
    ],
    'names': [
        {
            'name': 'ABC PLUMBING',
            'designation': 'LTD.',
            'choice': 1,
            'name_type_cd': 'CO',
            'consent_words': '',
            'conflict1': '',
            'conflict1_num': '',
        }
    ],
    'additionalInfo': '',
    'corpNum': '',
    'homeJurisNum': '',
    'natureBusinessInfo': 'Test',
    'previousRequestId': '',
    'tradeMark': '',
    'xproJurisdiction': '',
    'priorityCd': 'N',
    'entity_type': 'CR',
    'request_action': 'NEW',
    'stateCd': 'DRAFT',
    'english': True,
    'nameFlag': False,
    'submit_count': 0,
}


payment_post_data = {
    'paymentInfo': {'methodOfPayment': 'CC'},
    'businessInfo': {
        'corpType': 'NRO',
        'businessIdentifier': 'NR L000595',
        'businessName': 'ABC PLUMBING LTD.',
        'contactInfo': {
            'addressLine1': '1796 KINGS RD None',
            'city': 'VICTORIA',
            'province': 'BC',
            'country': 'CA',
            'postalCode': 'V8R 2P1',
        },
    },
    'filingInfo': {
        'date': '2020-07-26',
        'filingTypes': [
            {'filingTypeCode': 'NM620', 'priority': False, 'filingDescription': 'NM620: ABC PLUMBING LTD. ()'}
        ],
    },
}

get_after_payments_data = {
    'actions': ['EDIT', 'UPGRADE', 'REFUND', 'RECEIPT'],
    'additionalInfo': None,
    'applicants': {
        'addrLine1': '1796 KINGS RD',
        'addrLine2': None,
        'addrLine3': None,
        'city': 'VICTORIA',
        'clientFirstName': None,
        'clientLastName': None,
        'contact': '',
        'countryTypeCd': 'CA',
        'declineNotificationInd': None,
        'emailAddress': 'example@example.com',
        'faxNumber': None,
        'firstName': 'BOB',
        'lastName': 'JOHNSON',
        'middleName': None,
        'partyId': 1658430,
        'phoneNumber': '2505320083',
        'postalCd': 'V8R 2P1',
        'stateProvinceCd': 'BC',
    },
    'comments': [
        {
            'comment': 'The applicant has indicated the submitted name or names are in English.',
            'examiner': 'name_request_service_account',
            'id': 133464,
            'timestamp': 'Sun, 26 Jul 2020 22:56:17 GMT',
        }
    ],
    'consentFlag': None,
    'consent_dt': None,
    'corpNum': None,
    'entity_type_cd': 'CR',
    'expirationDate': None,
    'furnished': 'N',
    'hasBeenReset': False,
    'id': 2262943,
    'lastUpdate': 'Sun, 26 Jul 2020 22:56:27 GMT',
    'names': [
        {
            'choice': 1,
            'clean_name': None,
            'comment': None,
            'conflict1': '',
            'conflict1_num': '',
            'conflict2': '',
            'conflict2_num': '',
            'conflict3': '',
            'conflict3_num': '',
            'consumptionDate': None,
            'corpNum': None,
            'decision_text': '',
            'designation': 'LTD.',
            'id': 4264424,
            'name': 'ABC PLUMBING',
            'name_type_cd': 'CO',
            'state': 'NE',
        }
    ],
    'natureBusinessInfo': 'Test',
    'nrNum': 'NR L000597',
    'nwpta': [],
    'previousNr': None,
    'previousRequestId': None,
    'previousStateCd': None,
    'priorityCd': 'N',
    'priorityDate': None,
    'requestTypeCd': 'CR',
    'request_action_cd': 'NEW',
    'source': 'NAMEREQUEST',
    'state': 'DRAFT',
    'submitCount': 1,
    'submittedDate': 'Sun, 26 Jul 2020 22:56:17 GMT',
    'submitter_userid': 'name_request_service_account',
    'userId': 'name_request_service_account',
    'xproJurisdiction': None,
}

put_data = {
    'applicants': [
        {
            'addrLine1': '',
            'addrLine2': '',
            'city': '',
            'clientFirstName': '',
            'clientLastName': '',
            'contact': '',
            'countryTypeCd': '',
            'emailAddress': '',
            'faxNumber': '',
            'firstName': '',
            'lastName': '',
            'middleName': '',
            'phoneNumber': '',
            'postalCd': '',
            'stateProvinceCd': '',
        }
    ],
    'names': [
        {
            'choice': 1,
            'clean_name': None,
            'comment': None,
            'conflict1': '',
            'conflict1_num': '',
            'conflict2': '',
            'conflict2_num': '',
            'conflict3': '',
            'conflict3_num': '',
            'consumptionDate': None,
            'corpNum': None,
            'decision_text': '',
            'designation': 'LTD.',
            'id': 4264424,
            'name': 'ABC PLUMBING',
            'name_type_cd': 'CO',
            'state': 'NE',
            'consent_words': '',
        }
    ],
    'additionalInfo': '',
    'corpNum': '',
    'homeJurisNum': '',
    'natureBusinessInfo': '',
    'previousRequestId': '',
    'tradeMark': '',
    'xproJurisdiction': '',
    'priorityCd': 'N',
    'entity_type': 'CR',
    'request_action': 'NEW',
    'stateCd': 'DRAFT',
    'english': True,
    'nameFlag': False,
    'submit_count': 0,
}

put_response_data = {
    {
        'actions': None,
        'additionalInfo': None,
        'applicants': {
            'addrLine1': '1796 KINGS RD',
            'addrLine2': None,
            'addrLine3': None,
            'city': 'VICTORIA',
            'clientFirstName': None,
            'clientLastName': None,
            'contact': '',
            'countryTypeCd': 'CA',
            'declineNotificationInd': None,
            'emailAddress': 'example@example.com',
            'faxNumber': None,
            'firstName': 'BOB',
            'lastName': 'JOHNSON',
            'middleName': None,
            'partyId': 1658430,
            'phoneNumber': '2505320083',
            'postalCd': 'V8R 2P1',
            'stateProvinceCd': 'BC',
        },
        'comments': [
            {
                'comment': 'The applicant has indicated the submitted name or names are in English.',
                'examiner': 'name_request_service_account',
                'id': 133464,
                'timestamp': 'Sun, 26 Jul 2020 22:56:17 GMT',
            }
        ],
        'consentFlag': None,
        'consent_dt': None,
        'corpNum': None,
        'entity_type_cd': 'CR',
        'expirationDate': None,
        'furnished': 'N',
        'hasBeenReset': False,
        'id': 2262943,
        'lastUpdate': 'Sun, 26 Jul 2020 22:56:27 GMT',
        'names': [
            {
                'choice': 1,
                'clean_name': None,
                'comment': None,
                'conflict1': '',
                'conflict1_num': '',
                'conflict2': '',
                'conflict2_num': '',
                'conflict3': '',
                'conflict3_num': '',
                'consumptionDate': None,
                'corpNum': None,
                'decision_text': '',
                'designation': 'LTD.',
                'id': 4264424,
                'name': 'ABC PLUMBING',
                'name_type_cd': 'CO',
                'state': 'NE',
            }
        ],
        'natureBusinessInfo': 'Test',
        'nrNum': 'NR L000597',
        'nwpta': [],
        'previousNr': None,
        'previousRequestId': None,
        'previousStateCd': None,
        'priorityCd': 'N',
        'priorityDate': None,
        'requestTypeCd': 'CR',
        'request_action_cd': 'NEW',
        'source': 'NAMEREQUEST',
        'state': 'DRAFT',
        'submitCount': 1,
        'submittedDate': 'Sun, 26 Jul 2020 22:56:17 GMT',
        'submitter_userid': 'name_request_service_account',
        'userId': 'name_request_service_account',
        'xproJurisdiction': None,
    }
}

"""
{
    "additionalInfo": "Test initial",
    "names": [{
        "choice": 1,
        "clean_name": "",
        "comment": "",
        "conflict1": "",
        "conflict1_num": "",
        "conflict2": "",
        "conflict2_num": "",
        "conflict3": "",
        "conflict3_num": "",
        "consumptionDate": "",
        "corpNum": "",
        "decision_text": "",
        "designation": "LTD.",
        "id": 4264424,
        "name": "ABC PLUMBING",
        "name_type_cd": "CO",
        "state": "NE"
    }]
}
"""


"""
Actual patch:

"""

actual_patch = {
    'applicants': [
        {
            'addrLine1': '1796 KINGS RD',
            'addrLine2': None,
            'city': 'VICTORIA',
            'clientFirstName': None,
            'clientLastName': None,
            'contact': '',
            'countryTypeCd': 'CA',
            'emailAddress': 'example@example.com',
            'faxNumber': None,
            'firstName': 'BOB',
            'lastName': 'JOHNSON',
            'middleName': None,
            'phoneNumber': '2505320083',
            'postalCd': 'V8R2P1',
            'stateProvinceCd': 'BC',
            'addrLine3': None,
            'declineNotificationInd': None,
            'partyId': 1658443,
        }
    ],
    'names': [
        {
            'choice': 1,
            'clean_name': None,
            'comment': None,
            'conflict1': '',
            'conflict1_num': '',
            'conflict2': '',
            'conflict2_num': '',
            'conflict3': '',
            'conflict3_num': '',
            'consumptionDate': None,
            'corpNum': None,
            'decision_text': '',
            'designation': 'LTD.',
            'id': 4264448,
            'name': 'BLUE HERON TOURS',
            'name_type_cd': 'CO',
            'state': 'NE',
            'consent_words': '',
        },
        {
            'name': 'BLUE HERON ADVENTURE TOURS',
            'designation': 'LTD.',
            'choice': 2,
            'name_type_cd': 'CO',
            'consent_words': '',
            'conflict1': '',
            'conflict1_num': '',
        },
    ],
    'request_action_cd': 'NEW',
    'entity_type_cd': 'CR',
    'natureBusinessInfo': 'Test',
}

test_patch_initial = {
    'additionalInfo': 'Test initial',
    'names': [
        {
            'choice': 1,
            'clean_name': None,
            'comment': None,
            'conflict1': '',
            'conflict1_num': '',
            'conflict2': '',
            'conflict2_num': '',
            'conflict3': '',
            'conflict3_num': '',
            'consumptionDate': None,
            'corpNum': None,
            'decision_text': '',
            'designation': 'LTD.',
            'id': 4264424,
            'name': 'ABC PLUMBING',
            'name_type_cd': 'CO',
            'state': 'NE',
        }
    ],
}

test_patch_replace = {
    'additionalInfo': 'Test update',
    'names': [
        {
            'choice': 1,
            'clean_name': None,
            'comment': None,
            'conflict1': '',
            'conflict1_num': '',
            'conflict2': '',
            'conflict2_num': '',
            'conflict3': '',
            'conflict3_num': '',
            'consumptionDate': None,
            'corpNum': None,
            'decision_text': '',
            'designation': 'LTD.',
            'id': 4264424,
            'name': 'ABC PLUMBING EXPERTS',
            'name_type_cd': 'CO',
            'state': 'NE',
        }
    ],
}

# Just in here, i don't think this is super valuable to test separately
test_patch_edit = {
    'additionalInfo': 'Test update',
    'names': [
        {
            'choice': 1,
            'clean_name': None,
            'comment': None,
            'conflict1': '',
            'conflict1_num': '',
            'conflict2': '',
            'conflict2_num': '',
            'conflict3': '',
            'conflict3_num': '',
            'consumptionDate': None,
            'corpNum': None,
            'decision_text': '',
            'designation': 'LTD.',
            'id': 4264424,
            'name': 'ABC PLUMBING EXPERTS',
            'name_type_cd': 'CO',
            'state': 'NE',
        }
    ],
}

# PATCH
# http://localhost:5000/api/v1/namerequests/NR%20L000606/upgrade
# or
# http://localhost:5000/api/v1/namerequests/NR%20L000606/UPGRADE
test_patch_upgrade = {'additionalInfo': 'Test upgrade'}

# PATCH
# http://localhost:5000/api/v1/namerequests/NR%20L000606/cancel
# or
# http://localhost:5000/api/v1/namerequests/NR%20L000606/CANCEL
test_patch_cancel = {'additionalInfo': 'Test cancel'}

# PATCH
# http://localhost:5000/api/v1/namerequests/NR%20L000606/refund
# or
# http://localhost:5000/api/v1/namerequests/NR%20L000606/REFUND
test_patch_refund = {'additionalInfo': 'Test refund'}

# PATCH
# http://localhost:5000/api/v1/namerequests/NR%20L000606/reapply
# or
# http://localhost:5000/api/v1/namerequests/NR%20L000606/REAPPLY
test_patch_reapply = {'additionalInfo': 'Test reapply'}

# PATCH
# http://localhost:5000/api/v1/namerequests/NR%20L000606/resend
# or
# http://localhost:5000/api/v1/namerequests/NR%20L000606/RESEND
test_patch_resend = {'additionalInfo': 'Test resend'}
