class NameProcessingException(Exception):
    def __init__(self, wrapped_err=None, message="Name processing service error.", status_code=500):
        self.err = wrapped_err
        if wrapped_err:
            self.message = '{msg}\r\n\r\n{desc}'.format(msg=message, desc=str(wrapped_err))
        else:
            self.message = message
        # Map HTTP status if the wrapped error has an HTTP status code
        self.status_code = wrapped_err.status if wrapped_err and hasattr(wrapped_err, 'status') else status_code
        super().__init__(self.message)


class GetStopWordsApiError(NameProcessingException):
    def __init__(self, wrapped_err=None, message="Synonyms API get_stop_words call failed."):
        super().__init__(wrapped_err, message)


class GetPrefixesApiError(NameProcessingException):
    def __init__(self, wrapped_err=None, message="Synonyms API get_prefixes call failed."):
        super().__init__(wrapped_err, message)


class GetNumberWordsApiError(NameProcessingException):
    def __init__(self, wrapped_err=None, message="Synonyms API get_number_words call failed."):
        super().__init__(wrapped_err, message)


class GetStandAloneApiError(NameProcessingException):
    def __init__(self, wrapped_err=None, message="Synonyms API get_stand_alone call failed."):
        super().__init__(wrapped_err, message)


class GetDesignatedEndAllWordsApiError(NameProcessingException):
    def __init__(self, wrapped_err=None, message="Synonyms API get_designated_end_all_words call failed."):
        super().__init__(wrapped_err, message)


class GetDesignatedAnyAllWordsApiError(NameProcessingException):
    def __init__(self, wrapped_err=None, message="Synonyms API get_designated_any_all_words call failed."):
        super().__init__(wrapped_err, message)