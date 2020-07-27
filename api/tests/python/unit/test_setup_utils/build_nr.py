from namex.models import State, Request as RequestDAO, Name as NameDAO

test_names = [
    {'name': 'ABC PLUMBING', 'designation': 'LTD.'},
    {'name': 'ABC ENGINEERING', 'designation': 'LTD.'}
]


draft_data = {
    "applicants": [{
        "addrLine1": "1796 KINGS RD",
        "addrLine2": "",
        "city": "VICTORIA",
        "clientFirstName": "",
        "clientLastName": "",
        "contact": "",
        "countryTypeCd": "CA",
        "emailAddress": "lucaslopatka@gmail.com",
        "faxNumber": "",
        "firstName": "LUCAS",
        "lastName": "LOPATKA",
        "middleName": "",
        "phoneNumber": "2505320083",
        "postalCd": "V8R 2P1",
        "stateProvinceCd": "BC"
    }],
    "names": [{
        "name": "ABC PLUMBING",
        "designation": "LTD.",
        "choice": 1,
        "name_type_cd": "CO",
        "consent_words": "",
        "conflict1": "",
        "conflict1_num": ""
    }],
    "additionalInfo": "",
    "corpNum": "",
    "homeJurisNum": "",
    "natureBusinessInfo": "Test",
    "previousRequestId": "",
    "tradeMark": "",
    "xproJurisdiction": "",
    "priorityCd": "N",
    "entity_type": "CR",
    "request_action": "NEW",
    "stateCd": "DRAFT",
    "english": True,
    "nameFlag": False,
    "submit_count": 0
}


payment_post_data = {
    "paymentInfo": {
        "methodOfPayment": "CC"
    },
    "businessInfo": {
        "corpType": "NRO",
        "businessIdentifier": "NR L000595",
        "businessName": "ABC PLUMBING LTD.",
        "contactInfo": {
            "addressLine1": "1796 KINGS RD None",
            "city": "VICTORIA",
            "province": "BC",
            "country": "CA",
            "postalCode": "V8R 2P1"
        }
    },
    "filingInfo": {
        "date": "2020-07-26",
        "filingTypes": [{
            "filingTypeCode": "NM620",
            "priority": False,
            "filingDescription": "NM620: ABC PLUMBING LTD. ()"
        }]
    }

}

get_after_payments_data = {
    "actions": [
        "EDIT",
        "UPGRADE",
        "REFUND",
        "RECEIPT"
    ],
    "additionalInfo": None,
    "applicants": {
        "addrLine1": "1796 KINGS RD",
        "addrLine2": None,
        "addrLine3": None,
        "city": "VICTORIA",
        "clientFirstName": None,
        "clientLastName": None,
        "contact": "",
        "countryTypeCd": "CA",
        "declineNotificationInd": None,
        "emailAddress": "lucaslopatka@gmail.com",
        "faxNumber": None,
        "firstName": "LUCAS",
        "lastName": "LOPATKA",
        "middleName": None,
        "partyId": 1658430,
        "phoneNumber": "2505320083",
        "postalCd": "V8R 2P1",
        "stateProvinceCd": "BC"
    },
    "comments": [
        {
            "comment": "The applicant has indicated the submitted name or names are in English.",
            "examiner": "name_request_service_account",
            "id": 133464,
            "timestamp": "Sun, 26 Jul 2020 22:56:17 GMT"
        }
    ],
    "consentFlag": None,
    "consent_dt": None,
    "corpNum": None,
    "entity_type_cd": "CR",
    "expirationDate": None,
    "furnished": "N",
    "hasBeenReset": False,
    "id": 2262943,
    "lastUpdate": "Sun, 26 Jul 2020 22:56:27 GMT",
    "names": [
        {
            "choice": 1,
            "clean_name": None,
            "comment": None,
            "conflict1": "",
            "conflict1_num": "",
            "conflict2": "",
            "conflict2_num": "",
            "conflict3": "",
            "conflict3_num": "",
            "consumptionDate": None,
            "corpNum": None,
            "decision_text": "",
            "designation": "LTD.",
            "id": 4264424,
            "name": "ABC PLUMBING",
            "name_type_cd": "CO",
            "state": "NE"
        }
    ],
    "natureBusinessInfo": "Test",
    "nrNum": "NR L000597",
    "nwpta": [],
    "previousNr": None,
    "previousRequestId": None,
    "previousStateCd": None,
    "priorityCd": "N",
    "priorityDate": None,
    "requestTypeCd": "CR",
    "request_action_cd": "NEW",
    "source": "NAMEREQUEST",
    "state": "DRAFT",
    "submitCount": 1,
    "submittedDate": "Sun, 26 Jul 2020 22:56:17 GMT",
    "submitter_userid": "name_request_service_account",
    "userId": "name_request_service_account",
    "xproJurisdiction": None
}

put_data = {
    "applicants": [{
        "addrLine1": "",
        "addrLine2": "",
        "city": "",
        "clientFirstName": "",
        "clientLastName": "",
        "contact": "",
        "countryTypeCd": "",
        "emailAddress": "",
        "faxNumber": "",
        "firstName": "",
        "lastName": "",
        "middleName": "",
        "phoneNumber": "",
        "postalCd": "",
        "stateProvinceCd": ""
    }],
    "names": [{
        "choice": 1,
        "clean_name": None,
        "comment": None,
        "conflict1": "",
        "conflict1_num": "",
        "conflict2": "",
        "conflict2_num": "",
        "conflict3": "",
        "conflict3_num": "",
        "consumptionDate": None,
        "corpNum": None,
        "decision_text": "",
        "designation": "LTD.",
        "id": 4264424,
        "name": "ABC PLUMBING",
        "name_type_cd": "CO",
        "state": "NE",
        "consent_words": ""
    }],
    "additionalInfo": "",
    "corpNum": "",
    "homeJurisNum": "",
    "natureBusinessInfo": "",
    "previousRequestId": "",
    "tradeMark": "",
    "xproJurisdiction": "",
    "priorityCd": "N",
    "entity_type": "CR",
    "request_action": "NEW",
    "stateCd": "DRAFT",
    "english": True,
    "nameFlag": False,
    "submit_count": 0
}

put_response_data = {
    {
        "actions": None,
        "additionalInfo": None,
        "applicants": {
            "addrLine1": "1796 KINGS RD",
            "addrLine2": None,
            "addrLine3": None,
            "city": "VICTORIA",
            "clientFirstName": None,
            "clientLastName": None,
            "contact": "",
            "countryTypeCd": "CA",
            "declineNotificationInd": None,
            "emailAddress": "lucaslopatka@gmail.com",
            "faxNumber": None,
            "firstName": "LUCAS",
            "lastName": "LOPATKA",
            "middleName": None,
            "partyId": 1658430,
            "phoneNumber": "2505320083",
            "postalCd": "V8R 2P1",
            "stateProvinceCd": "BC"
        },
        "comments": [
            {
                "comment": "The applicant has indicated the submitted name or names are in English.",
                "examiner": "name_request_service_account",
                "id": 133464,
                "timestamp": "Sun, 26 Jul 2020 22:56:17 GMT"
            }
        ],
        "consentFlag": None,
        "consent_dt": None,
        "corpNum": None,
        "entity_type_cd": "CR",
        "expirationDate": None,
        "furnished": "N",
        "hasBeenReset": False,
        "id": 2262943,
        "lastUpdate": "Sun, 26 Jul 2020 22:56:27 GMT",
        "names": [
            {
                "choice": 1,
                "clean_name": None,
                "comment": None,
                "conflict1": "",
                "conflict1_num": "",
                "conflict2": "",
                "conflict2_num": "",
                "conflict3": "",
                "conflict3_num": "",
                "consumptionDate": None,
                "corpNum": None,
                "decision_text": "",
                "designation": "LTD.",
                "id": 4264424,
                "name": "ABC PLUMBING",
                "name_type_cd": "CO",
                "state": "NE"
            }
        ],
        "natureBusinessInfo": "Test",
        "nrNum": "NR L000597",
        "nwpta": [],
        "previousNr": None,
        "previousRequestId": None,
        "previousStateCd": None,
        "priorityCd": "N",
        "priorityDate": None,
        "requestTypeCd": "CR",
        "request_action_cd": "NEW",
        "source": "NAMEREQUEST",
        "state": "DRAFT",
        "submitCount": 1,
        "submittedDate": "Sun, 26 Jul 2020 22:56:17 GMT",
        "submitter_userid": "name_request_service_account",
        "userId": "name_request_service_account",
        "xproJurisdiction": None
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

test_patch_initial = {
    "additionalInfo": "Test initial",
    "names": [{
        "choice": 1,
        "clean_name": None,
        "comment": None,
        "conflict1": "",
        "conflict1_num": "",
        "conflict2": "",
        "conflict2_num": "",
        "conflict3": "",
        "conflict3_num": "",
        "consumptionDate": None,
        "corpNum": None,
        "decision_text": "",
        "designation": "LTD.",
        "id": 4264424,
        "name": "ABC PLUMBING",
        "name_type_cd": "CO",
        "state": "NE"
    }]
}

test_patch_replace = {
    "additionalInfo": "Test update",
    "names": [{
        "choice": 1,
        "clean_name": None,
        "comment": None,
        "conflict1": "",
        "conflict1_num": "",
        "conflict2": "",
        "conflict2_num": "",
        "conflict3": "",
        "conflict3_num": "",
        "consumptionDate": None,
        "corpNum": None,
        "decision_text": "",
        "designation": "LTD.",
        "id": 4264424,
        "name": "ABC PLUMBING EXPERTS",
        "name_type_cd": "CO",
        "state": "NE"
    }]
}

def build_nr(nr_state):
    """
    Creates an NR in a given state.
    :param nr_state:
    :return:
    """
    return {
        State.DRAFT: build_draft,
        State.RESERVED: build_reserved,
        State.COND_RESERVE: build_cond_reserved,
        State.CONDITIONAL: build_conditional,
        State.APPROVED: build_approved
    }.get(nr_state)()


def build_draft():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.DRAFT
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = test_names[0].get('name')
    nr.names = [name1]

    return nr


def build_cond_reserved():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.COND_RESERVE
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = test_names[0].get('name')
    nr.names = [name1]

    return nr


def build_reserved():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.RESERVED
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = test_names[0].get('name')
    nr.names = [name1]

    return nr


def build_conditional():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.CONDITIONAL
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = test_names[0].get('name')
    nr.names = [name1]

    return nr


def build_approved():
    nr = RequestDAO()
    nr.nrNum = 'NR 0000002'
    nr.stateCd = State.APPROVED
    nr.requestId = 1460775
    nr._source = 'NRO'
    name1 = NameDAO()
    name1.choice = 1
    name1.name = test_names[0].get('name')
    nr.names = [name1]

    return nr
