"""Application Specific Exceptions, to manage the business errors

@log_error - a decorator to automatically log the exception to the logger provided

BusinessException - error, status_code - Business rules error
   error - a description of the error {code / description: classname / full text}
   status_code - where possible use HTTP Error Codes

"""

import functools


class BusinessException(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def log_error(logger):
    def decorated(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.exception(e)
                raise

        return wrapped

    return decorated


class EntityServiceException(Exception):
    """get business info"""

    def __init__(self, wrapped_err=None, message='Entity API exception.', status_code=500):
        self.err = wrapped_err
        self.colin_error_code = None
        self.status_code = status_code

        if wrapped_err and hasattr(wrapped_err, 'status'):
            # Map HTTP status if the wrapped error has an HTTP status code
            self.status_code = wrapped_err.status if wrapped_err.status else status_code

        if wrapped_err and hasattr(wrapped_err, 'error_code'):
            # Map COLIN error code if the wrapped error has a COLIN error code
            self.error_code = int(wrapped_err.error_code)

        if wrapped_err and hasattr(wrapped_err, 'internal_error_code'):
            # Map COLIN error code if the wrapped error has a COLIN error code
            self.colin_error_code = int(wrapped_err.internal_error_code)

        if self.colin_error_code is not None:
            self.message = (
                message if message else str(self.colin_error_code) + ': ' + wrapped_err['internal_error_message']
            )
        elif wrapped_err:
            self.message = '{msg}\r\n\r\n{desc}'.format(msg=message, desc=str(wrapped_err))
        else:
            self.message = message

        super().__init__(self.message)
