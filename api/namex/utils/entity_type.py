"""
These are common utilities shared across Namex projects. Any utilities that are common to multiple services should
either reside here, or be imported and exported from here.
"""

# TODO: Implement a true shared lib for stuff like this!
#  Most, if not all of these methods are shared with the namex api project!
from namex.constants import (
    BCProtectedNameEntityTypes,
    BCUnprotectedNameEntityTypes,
    XproUnprotectedNameEntityTypes,
    EntityTypes,
    EntityTypeDescriptions,
    DesignationPositionCodes,
)

"""
A temporary fallback for getting an EntityType code using its string value.
This method will be removed in a future iteration. Please use get_entity_type_code.
"""


def get_entity_type_code_DEPRECATED(entity_type_str):
    entity_type_code = None
    if BCProtectedNameEntityTypes.has_value(entity_type_str):
        entity_type_code = BCProtectedNameEntityTypes(entity_type_str)
    elif BCUnprotectedNameEntityTypes.has_value(entity_type_str):
        entity_type_code = BCUnprotectedNameEntityTypes(entity_type_str)
    elif XproUnprotectedNameEntityTypes.has_value(entity_type_str):
        entity_type_code = XproUnprotectedNameEntityTypes(entity_type_str)

    return entity_type_code


def get_entity_type_code(entity_type_str):
    entity_type_code = None
    if EntityTypes.has_value(entity_type_str):
        entity_type_code = EntityTypes(entity_type_str)

    return entity_type_code


def get_designation_position_code(position_code_str):
    position_code = None
    if DesignationPositionCodes.has_value(position_code_str):
        position_code = DesignationPositionCodes(position_code_str)

    return position_code


def get_entity_type_code_description(entity_type_code):
    entity_type_code_description = ''
    if EntityTypeDescriptions.get(entity_type_code):
        entity_type_code_description = EntityTypeDescriptions[entity_type_code]

    return entity_type_code_description


"""
A wrapper for get_entity_type_code_description that provides the ability to get an
EntityType code description using its text / string value, as opposed to the code itself.
"""


def get_entity_type_description(entity_type_str):
    entity_type_code = get_entity_type_code(entity_type_str)
    return get_entity_type_code_description(entity_type_code) if entity_type_code else ''
