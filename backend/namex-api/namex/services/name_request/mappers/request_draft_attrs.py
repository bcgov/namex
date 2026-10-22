from datetime import datetime

from namex.services.name_request.exceptions import MapRequestDataError


def map_draft_attrs(name_request, **kwargs):
    """
    Used internally by map_request_data.
    :param name_request:
    :return:
    """
    try:
        user_id = kwargs.get('user_id')
        # Set this to name_request_service_account
        name_request.userId = user_id
        name_request.submittedDate = datetime.utcnow()
    except Exception as err:
        raise MapRequestDataError(err)

    return name_request
