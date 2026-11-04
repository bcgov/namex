class NameRequestException(Exception):
    def __init__(self, wrapped_err=None, message='Name request error.', status_code=500):
        self.err = wrapped_err
        if wrapped_err:
            self.message = '{msg}\r\n\r\n{desc}'.format(msg=message, desc=str(wrapped_err))
        else:
            self.message = message
        # Map HTTP status if the wrapped error has an HTTP status code
        self.status_code = wrapped_err.status if wrapped_err and hasattr(wrapped_err, 'status') else status_code
        super().__init__(self.message)


class NameRequestIsInProgressError(NameRequestException):
    def __init__(self, wrapped_err=None, message='The name request is INPROGESS and is locked for editing.'):
        super().__init__(wrapped_err, message)


class NameRequestActionError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error building request actions.'):
        super().__init__(wrapped_err, message)


class NameRequestPaymentError(NameRequestException):
    def __init__(self, wrapped_err=None, message='SBC Pay API error.'):
        super().__init__(wrapped_err, message)


class NameRequestIsExpiredError(NameRequestException):
    def __init__(self, wrapped_err=None, message='The request is expired.'):
        super().__init__(wrapped_err, message)


class NameRequestIsConsumedError(NameRequestException):
    def __init__(self, wrapped_err=None, message='The request has already been consumed.'):
        super().__init__(wrapped_err, message)


class GenerateNRKeysError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error generating NR keys.'):
        super().__init__(wrapped_err, message)


class InvalidInputError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error getting json input.'):
        super().__init__(wrapped_err, message)


class InvalidStateError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Invalid state error.'):
        super().__init__(wrapped_err, message)


class CreateNameRequestError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error initializing name_request object.'):
        super().__init__(wrapped_err, message)


class MapRequestTypeError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error mapping the request type.'):
        super().__init__(wrapped_err, message)


class MapRequestDataError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error setting reserve state.'):
        super().__init__(wrapped_err, message)


class MapRequestHeaderAttributesError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error setting request header attributes.'):
        super().__init__(wrapped_err, message)


class MapRequestAttributesError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error setting request attributes.'):
        super().__init__(wrapped_err, message)


class MapLanguageCommentError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error setting language comment.'):
        super().__init__(wrapped_err, message)


class MapPersonCommentError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error setting person name comment'):
        super().__init__(wrapped_err, message)


class UpdateSubmitCountError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error setting submit count.'):
        super().__init__(wrapped_err, message)


class ExtendExpiryDateError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error extending the expiry date.'):
        super().__init__(wrapped_err, message)


class MapRequestNamesError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error setting names.'):
        super().__init__(wrapped_err, message)


class MapRequestApplicantError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error setting applicant.'):
        super().__init__(wrapped_err, message)


class SolrUpdateError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error updating solr for reservation.'):
        super().__init__(wrapped_err, message)


class SaveNameRequestError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error saving request.'):
        super().__init__(wrapped_err, message)


class GetUserIdError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error getting user id.'):
        super().__init__(wrapped_err, message)


class VirtualWordConditionServiceError(NameRequestException):
    def __init__(self, wrapped_err=None, message='Error initializing VirtualWordCondition Service.'):
        super().__init__(wrapped_err, message)


# exception raising for existing request by same name and by same user email
class NameRequestIsAlreadySubmittedError(NameRequestException):
    def __init__(self, wrapped_err=None, message='The request with same name is already submitted.'):
        super().__init__(wrapped_err, message)
