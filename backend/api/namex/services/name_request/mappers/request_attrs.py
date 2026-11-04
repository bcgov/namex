from namex.services.name_request.exceptions import MapRequestAttributesError

from ..utils import get_mapped_request_type

NAME_REQUEST_SOURCE = 'NAMEREQUEST'


def map_request_attrs(name_request, **kwargs):
    """
    Used internally by map_request_data.
    :param name_request:
    :key nr_id: int
    :key nr_num: str
    :key request_entity: str
    :key request_action: str
    :key request_type: str
    :return:
    """
    try:
        # Use class property values for the ID, NR Number and Source!
        # Do not map those values from the request if supplied, as they
        # should not be changed outside of the context of this application!
        nr_id = kwargs.get('nr_id')
        nr_num = kwargs.get('nr_num')
        name_request.id = nr_id
        name_request.nrNum = nr_num
        name_request._source = NAME_REQUEST_SOURCE

        # Default to whatever entity, action, or type already exists when mapping
        request_entity = kwargs.get('request_entity', name_request.entity_type_cd)
        request_action = kwargs.get('request_action', name_request.request_action_cd)
        request_type = kwargs.get('request_type', name_request.requestTypeCd)

        conversion_type = kwargs.get('conversion_type', None)

        # Set action and entity
        if request_entity:
            name_request.entity_type_cd = request_entity

        if request_action:
            name_request.request_action_cd = request_action

        # TODO: Throw exceptions for invalid combos?
        if not request_type and request_entity and request_action:
            # If request_type is None (eg. no 'requestTypeCd' was provided in the payload)
            # but a request_entity (entity_type_cd) and a request_action (request_action_cd)
            # are supplied, use get_mapped_request_type to map the requestTypeCd in the model
            # using the action and entity type

            # if conversion_type exists, using conversion_type as request_type
            if conversion_type:
                name_request.requestTypeCd = conversion_type
            else:
                request_type = get_mapped_request_type(request_entity, request_action)
                name_request.requestTypeCd = request_type[0]
        elif request_type is not None:
            # If request_type is NOT None, (eg. 'requestTypeCd' was provided in the payload)
            # then use the provided value
            name_request.requestTypeCd = request_type
    except Exception as err:
        raise MapRequestAttributesError(err)

    return name_request
