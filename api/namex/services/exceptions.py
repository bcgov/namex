# Format error response and append status code.
class ServicesError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class ApiServiceException(Exception):
    def __init__(self, wrapped_err=None, message='API service error.'):
        self.err = wrapped_err
        self.message = message
        super().__init__(self.message)
