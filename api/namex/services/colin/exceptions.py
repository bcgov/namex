"""Format error response and append status code."""


class ColinServicesError(Exception):
    """Oracle Service Error Object."""

    def __init__(self, error, status_code):
        """Initialize."""
        self.error = error
        self.status_code = status_code
