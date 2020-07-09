class NameRequestException(Exception):
    def __init__(self, wrapped_err, message="Error setting request header attributes."):
        self.err = wrapped_err
        self.message = message
        super().__init__(self.message)


class InvalidInputError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error getting json input."):
        super().__init__(wrapped_err, message)


class CreateNameRequestError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error initializing name_request object."):
        super().__init__(wrapped_err, message)


class MapRequestDataError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error setting reserve state."):
        super().__init__(wrapped_err, message)


class MapRequestHeaderAttributesError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error setting request header attributes."):
        super().__init__(wrapped_err, message)


class MapRequestAttributesError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error setting request attributes."):
        super().__init__(wrapped_err, message)


class MapLanguageCommentError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error setting language comment."):
        super().__init__(wrapped_err, message)


class MapPersonCommentError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error setting person name comment"):
        super().__init__(wrapped_err, message)


class UpdateSubmitCountError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error setting submit count."):
        super().__init__(wrapped_err, message)


class MapRequestNamesError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error setting names."):
        super().__init__(wrapped_err, message)


class SolrUpdateError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error updating solr for reservation."):
        super().__init__(wrapped_err, message)


class NROUpdateError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error updating NRO (Oracle). You must re-try."):
        super().__init__(wrapped_err, message)


class SaveNameRequestError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error saving request."):
        super().__init__(wrapped_err, message)


class GetUserIdError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error getting user id."):
        super().__init__(wrapped_err, message)


class VirtualWordContidionServiceError(NameRequestException):
    def __init__(self, wrapped_err=None, message="Error initializing VirtualWordCondition Service."):
        super().__init__(wrapped_err, message)
