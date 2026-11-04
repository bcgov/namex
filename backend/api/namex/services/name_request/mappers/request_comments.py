from namex.models import Comment
from namex.services.name_request.exceptions import MapLanguageCommentError, MapPersonCommentError


def build_language_comment(english_bol, user_id, nr_id):
    lang_comment = Comment()
    lang_comment.examinerId = user_id
    lang_comment.nrId = nr_id
    if english_bol is True:
        # Add a comment for the examiner that says this is not an english name
        lang_comment.comment = 'The applicant has indicated the submitted name or names are in English.'
    else:
        lang_comment.comment = 'The applicant has indicated the submitted name or names are not English.'
    return lang_comment


def build_name_comment(user_id, nr_id):
    name_comment = Comment()
    name_comment.examinerId = user_id
    name_comment.nrId = nr_id
    name_comment.comment = 'The submitted name or names is a person name, coined phrase or trademark'
    return name_comment


def map_request_comments(name_request, **kwargs):
    """
    Used internally by map_request_data. Execute any logic required to map comments here.
    :param name_request:
    :return:
    """
    name_request = _map_request_language_comments(name_request, **kwargs)
    name_request = _map_request_person_name_comments(name_request, **kwargs)

    return name_request


def _map_request_language_comments(name_request, **kwargs):
    """
    Used internally by map_request_comments.
    :param name_request:
    :key request_data: dict
    :key user_id:
    :key nr_id: int
    :return:
    """
    try:
        request_data = kwargs.get('request_data')
        user_id = kwargs.get('user_id')
        nr_id = kwargs.get('nr_id')

        # If the language comment exists, we don't need to add it again
        if request_data.get('english') is not None:
            lang_comment = build_language_comment(request_data.get('english'), user_id, nr_id)
            matching_comments = list(filter(lambda x: x.comment == lang_comment.comment, list(name_request.comments)))
            if len(matching_comments) == 0:
                name_request.comments.append(lang_comment)
    except Exception as err:
        raise MapLanguageCommentError(err)

    return name_request


def _map_request_person_name_comments(name_request, **kwargs):
    """
    Used internally by map_request_comments.
    :param name_request:
    :key request_data: dict
    :key user_id:
    :key nr_id: int
    :return:
    """
    try:
        request_data = kwargs.get('request_data')
        user_id = kwargs.get('user_id')
        nr_id = kwargs.get('nr_id')

        if request_data.get('nameFlag') is not None:
            if request_data.get('nameFlag') is True:
                # If the person name comment exists, we don't need to add it again
                name_comment = build_name_comment(user_id, nr_id)
                matching_comments = list(
                    filter(lambda x: x.comment == name_comment.comment, list(name_request.comments))
                )
                if len(matching_comments) == 0:
                    name_request.comments.append(name_comment)
    except Exception as err:
        raise MapPersonCommentError(err)

    return name_request
