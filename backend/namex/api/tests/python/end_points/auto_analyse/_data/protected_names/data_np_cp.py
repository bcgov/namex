def data_for_add_distinctive_word_request_test():
    return {'name': 'FOOD GROWERS INC.', 'location': 'BC', 'entity_type_cd': 'CP', 'request_action_cd': 'NEW'}


def data_for_add_descriptive_word_request_test():
    return {'name': 'MOUNTAIN VIEW INC.', 'location': 'BC', 'entity_type_cd': 'CP', 'request_action_cd': 'NEW'}


def data_for_too_many_words_request_test():
    return {
        'name': 'MOUNTAIN VIEW FOOD GROWERS INTERNATIONAL INC.',
        'location': 'BC',
        'entity_type_cd': 'CP',
        'request_action_cd': 'NEW',
    }


def data_for_contains_words_to_avoid_request_test():
    return {
        'name': 'MOUNTAIN VIEW VSC INC.',  # VSC = VANCOUVER STOCK EXCHANGE
        'location': 'BC',
        'entity_type_cd': 'CP',
        'request_action_cd': 'NEW',
    }


def data_for_designation_mismatch_request_test():
    return {
        'name': 'MOUNTAIN VIEW FOOD GROWERS INC.',
        'location': 'BC',
        'entity_type_cd': 'CP',
        'request_action_cd': 'NEW',
    }


def data_for_name_requires_consent_request_test():
    return {
        'name': 'MOUNTAIN VIEW FOOD ENGINEERING INC.',
        'location': 'BC',
        'entity_type_cd': 'CP',
        'request_action_cd': 'NEW',
    }


# TODO: Pytest uses an empty DB so create a CONFLICTING NAME first before / as part of running this test!!!


def data_for_contains_unclassifiable_word_request_test():
    # TODO: Insert 'name': 'MOUNTAIN VIEW FOOD INC.' as the 1st test!
    # TODO: Insert 'name': 'MOUNTAIN VIEW GROWERS INC.' as the 2nd test!
    return {
        'name': 'MOUNTAIN VIEW FOOD BLOGGINS INC.',
        'location': 'BC',
        'entity_type_cd': 'CP',
        'request_action_cd': 'NEW',
    }


def data_for_corporate_name_conflict_request_test():
    return {
        'name': 'MOUNTAIN VIEW FOOD GROWERS INC.',
        'location': 'BC',
        'entity_type_cd': 'CP',
        'request_action_cd': 'NEW',
    }
