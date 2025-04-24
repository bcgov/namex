from flask_restx import fields
from .api_namespace import api

applicant_model = api.model(
    'applicant_model',
    {
        'partyId': fields.Integer('partyId'),
        'lastName': fields.String(attribute='lastName'),
        'firstName': fields.String(attribute='firstName'),
        'middleName': fields.String('Applicant middle name or initial'),
        'contact': fields.String('Applicant contact person last and first name'),
        'clientFirstName': fields.String('Client first name'),
        'clientLastName': fields.String('Client last name'),
        'phoneNumber': fields.String('Contact phone number'),
        'faxNumber': fields.String('Contact fax number'),
        'emailAddress': fields.String('Contact email'),
        'addrLine1': fields.String('First address line'),
        'addrLine2': fields.String('Second address line'),
        'city': fields.String('City'),
        'stateProvinceCd': fields.String('Province or state code'),
        'postalCd': fields.String('Postal code or zip code'),
        'countryTypeCd': fields.String('Country code'),
    },
)

consent_model = api.model('consent_model', {'consent_word': fields.String('A word that requires consent')})

name_model = api.model(
    'name_model',
    {
        'id': fields.Integer('id'),
        'choice': fields.Integer('Name choice'),
        'name': fields.String('Name'),
        'name_type_cd': fields.String('For company or assumed name', enum=['CO', 'AS']),
        'state': fields.String('The state of the Name'),
        'designation': fields.String('Name designation based on entity type'),
        'conflict1_num': fields.String('The corp_num of the matching name'),
        'conflict1': fields.String('The matching corp name'),
        'consent_words': fields.Nested(consent_model),
        'corpNum': fields.String('Corp Num'),
    },
)

nr_request = api.model(
    'name_request',
    {
        'id': fields.Integer('id'),
        'nrNum': fields.Integer('nrNum'),
        'entity_type_cd': fields.String('The entity type'),
        'request_action_cd': fields.String('The action requested by the user'),
        'stateCd': fields.String('The state of the NR'),
        'english': fields.Boolean('Set when the name is English only'),
        'nameFlag': fields.Boolean('Set when the name is a person'),
        'additionalInfo': fields.String('Additional NR Info'),
        'natureBusinessInfo': fields.String('The nature of business'),
        'tradeMark': fields.String('Registered Trademark'),
        'previousRequestId': fields.Integer('Internal Id for Re-Applys'),
        'priorityCd': fields.String('Set to Yes if it is  priority going to examination'),
        'submit_count': fields.Integer('Used to enforce the 3 times only rule for Re-Applys'),
        'xproJurisdiction': fields.String('The province or country code for XPRO requests'),
        'homeJurisNum': fields.String('For MRAS participants, their home jurisdiction corp_num'),
        'corpNum': fields.String('For companies already registered in BC, their BC corp_num'),
        'applicants': fields.Nested(applicant_model),
        'names': fields.Nested(name_model),
    },
)
