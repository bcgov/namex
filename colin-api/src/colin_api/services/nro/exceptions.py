"""Format error response and append status code."""


class NROServicesError(Exception):
    """NRO Service Error Object."""

    def __init__(self, error, status_code):
        """Initialize."""
        self.error = error
        self.status_code = status_code
