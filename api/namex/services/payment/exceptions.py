class PaymentException(Exception):
    """
    Base class for Payment exceptions.
    """
    def __init__(self, wrapped_err=None, message="Payment exception.", status_code=None):
        self.err = wrapped_err
        self.message = message
        self.status_code = wrapped_err.status if wrapped_err else 500
        super().__init__(self.message)


class PaymentServiceError(PaymentException):
    """
    Used for Namex Payment service errors.
    """
    def __init__(self, wrapped_err=None, message="Payment Service error."):
        super().__init__(wrapped_err, message)


class SBCPaymentException(PaymentException):
    """
    Used for general / unknown Service BC Payment API exceptions when calling the Service BC Payment API.
    """
    def __init__(self, wrapped_err=None, message="Unhandled SBC Pay API exception."):
        super().__init__(wrapped_err, message)


class SBCPaymentError(PaymentException):
    """
    Used for known Service BC Payment API errors when calling the Service BC Payment API,
    when the response contains a specific error message / code.
    """
    def __init__(self, wrapped_err=None, message="SBC Pay API error."):
        super().__init__(wrapped_err, message)
