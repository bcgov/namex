def data_for_contains_unclassifiable_word_request_test():
    return {
        'name': 'MOUNTAIN VIEW FOOD BLOGGINS ULC.',
        'location': 'CA',
        'entity_type_cd': 'XUL',
        'request_action_cd': 'NEW',
    }


def data_for_contains_words_to_avoid_request_test():
    return {'name': 'MOUNTAIN VIEW VSC ULC.', 'location': 'CA', 'entity_type_cd': 'XUL', 'request_action_cd': 'NEW'}


def data_for_name_requires_consent_request_test():
    return {
        'name': 'MOUNTAIN VIEW FOOD ENGINEERING ULC.',
        'location': 'CA',
        'entity_type_cd': 'XUL',
        'request_action_cd': 'NEW',
    }


def data_for_corporate_name_conflict_request_test():
    return {
        'name': 'MOUNTAIN VIEW FOOD GROWERS ULC.',
        'location': 'CA',
        'entity_type_cd': 'XUL',
        'request_action_cd': 'NEW',
    }
