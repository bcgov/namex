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