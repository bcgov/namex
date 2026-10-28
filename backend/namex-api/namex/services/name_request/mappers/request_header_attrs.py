from datetime import datetime

from namex.services.name_request.exceptions import MapRequestHeaderAttributesError
from namex.utils.common import convert_to_ascii


def map_request_header_attrs(name_request, **kwargs):
    """
    Used internally by map_request_data.
    :param name_request:
    :return:
    """
    request_data = kwargs.get('request_data')
    user_id = kwargs.get('user_id')

    try:
        # TODO: Review additional info stuff from NRO/namex (prev NR for re-applies,no NWPTA?
        if isinstance(request_data.get('natureBusinessInfo'), str):
            name_request.natureBusinessInfo = convert_to_ascii(request_data.get('natureBusinessInfo'))
        if isinstance(request_data.get('additionalInfo'), str):
            name_request.additionalInfo = convert_to_ascii(request_data.get('additionalInfo'))
        if isinstance(request_data.get('tradeMark'), str):
            name_request.tradeMark = request_data.get('tradeMark')
        if isinstance(request_data.get('previousRequestId'), int):
            name_request.previousRequestId = request_data.get('previousRequestId')
        if isinstance(request_data.get('priorityCd'), str):
            name_request.priorityCd = request_data.get('priorityCd')
        if request_data.get('priorityCd') == 'Y':
            name_request.priorityDate = datetime.utcnow().date()

        name_request.submitter_userid = user_id

        # XPRO
        if isinstance(request_data.get('xproJurisdiction'), str):
            name_request.xproJurisdiction = request_data.get('xproJurisdiction')
        # For MRAS participants
        if isinstance(request_data.get('homeJurisNum'), str):
            name_request.homeJurisNum = convert_to_ascii(request_data.get('homeJurisNum'))
        # For existing businesses
        if isinstance(request_data.get('corpNum'), str):
            name_request.corpNum = convert_to_ascii(request_data.get('corpNum'))
    except Exception as err:
        raise MapRequestHeaderAttributesError(err)

    return name_request
