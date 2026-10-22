# TODO: Maybe we need this test, maybe we don't we may just actually want to flag the unclassifiable words here...


def data_for_contains_unclassifiable_word_request_test():
    return {
        'name': 'MOUNTAIN VIEW FOOD BLOGGINS COOP',
        'location': 'CA',
        'entity_type_cd': 'XCP',
        'request_action_cd': 'NEW',
    }


def data_for_contains_words_to_avoid_request_test():
    return {'name': 'MOUNTAIN VIEW VSC COOP', 'location': 'CA', 'entity_type_cd': 'XCP', 'request_action_cd': 'NEW'}


def data_for_name_requires_consent_request_test():
    return {
        'name': 'MOUNTAIN VIEW FOOD ENGINEERING COOP',
        'location': 'CA',
        'entity_type_cd': 'XCP',
        'request_action_cd': 'NEW',
    }


def data_for_corporate_name_conflict_request_test():
    return {
        'name': 'MOUNTAIN VIEW FOOD GROWERS COOP',
        'location': 'CA',
        'entity_type_cd': 'XCP',
        'request_action_cd': 'NEW',
    }
