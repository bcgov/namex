from namex.utils.common import convert_to_ascii
from namex.models import Applicant


def map_request_applicant(applicant: Applicant, request_applicant: dict):
    applicant.lastName = convert_to_ascii(request_applicant.get('lastName'))
    applicant.firstName = convert_to_ascii(request_applicant.get('firstName'))
    applicant.middleName = convert_to_ascii(request_applicant.get('middleName')) if request_applicant.get('middleName') else None
    applicant.contact = convert_to_ascii(request_applicant.get('contact')) if request_applicant.get('contact') else None

    applicant.clientFirstName = convert_to_ascii(request_applicant.get('clientFirstName')) if request_applicant.get('clientFirstName') else None
    applicant.clientLastName = convert_to_ascii(request_applicant.get('clientLastName')) if request_applicant.get('clientLastName') else None

    applicant.phoneNumber = convert_to_ascii(request_applicant.get('phoneNumber'))
    applicant.faxNumber = convert_to_ascii(request_applicant.get('faxNumber')) if request_applicant.get('faxNumber') else None
    applicant.emailAddress = convert_to_ascii(request_applicant.get('emailAddress'))

    applicant.addrLine1 = convert_to_ascii(request_applicant.get('addrLine1'))
    applicant.addrLine2 = convert_to_ascii(request_applicant.get('addrLine2')) if request_applicant.get('addrLine2') else None
    applicant.addrLine3 = convert_to_ascii(request_applicant.get('addrLine3')) if request_applicant.get('addrLine3') else None
    applicant.city = convert_to_ascii(request_applicant.get('city'))
    applicant.stateProvinceCd = request_applicant.get('stateProvinceCd')
    applicant.postalCd = convert_to_ascii(request_applicant.get('postalCd'))
    applicant.countryTypeCd = request_applicant.get('countryTypeCd')

    return applicant
