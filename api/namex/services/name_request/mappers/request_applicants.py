from namex.utils.common import convert_to_ascii
from namex.models import Applicant


def map_request_applicant(applicant: Applicant, request_applicant: dict):
    applicant.lastName = convert_to_ascii(request_applicant.get('lastName'))
    applicant.firstName = convert_to_ascii(request_applicant.get('firstName'))
    if request_applicant.get('middleName'):
        applicant.middleName = convert_to_ascii(request_applicant.get('middleName'))
    applicant.contact = convert_to_ascii(request_applicant.get('contact'))

    if request_applicant.get('clientFirstName'):
        applicant.clientFirstName = convert_to_ascii(request_applicant.get('clientFirstName'))
    if request_applicant.get('clientLastName'):
        applicant.clientLastName = convert_to_ascii(request_applicant.get('clientLastName'))

    if request_applicant.get('phoneNumber'):
        applicant.phoneNumber = convert_to_ascii(request_applicant.get('phoneNumber'))
    if request_applicant.get('faxNumber'):
        applicant.faxNumber = convert_to_ascii(request_applicant.get('faxNumber'))
    applicant.emailAddress = convert_to_ascii(request_applicant.get('emailAddress'))

    applicant.addrLine1 = convert_to_ascii(request_applicant.get('addrLine1'))
    if request_applicant.get('addrLine2'):
        applicant.addrLine2 = convert_to_ascii(request_applicant.get('addrLine2'))
    if request_applicant.get('addrLine3'):
        applicant.addrLine3 = convert_to_ascii(request_applicant.get('addrLine3'))
    applicant.city = convert_to_ascii(request_applicant.get('city'))
    applicant.stateProvinceCd = request_applicant.get('stateProvinceCd')
    applicant.postalCd = convert_to_ascii(request_applicant.get('postalCd'))
    applicant.countryTypeCd = request_applicant.get('countryTypeCd')

    return applicant
