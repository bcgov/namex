class PaymentException(Exception):
    def __init__(self, wrapped_err=None, message="Payment exception."):
        self.err = wrapped_err
        self.message = message
        super().__init__(self.message)


class PaymentServiceError(PaymentException):
    def __init__(self, wrapped_err=None, message="Payment Service error."):
        super().__init__(wrapped_err, message)


class SBCPaymentException(PaymentException):
    def __init__(self, wrapped_err=None, message="Payment Service exception."):
        super().__init__(wrapped_err, message)


class SBCPaymentError(PaymentException):
    def __init__(self, wrapped_err=None, message="SBC Pay API error."):
        super().__init__(wrapped_err, message)
