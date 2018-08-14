# Format error response and append status code.
class ServicesError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code