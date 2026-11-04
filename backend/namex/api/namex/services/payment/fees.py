from flask import current_app

from .client import SBCPaymentClient
from .exceptions import SBCPaymentException
from .models.abstract import Serializable


class CalculateFeesRequest(Serializable):
    def __init__(self, **kwargs):
        self.corp_type = kwargs.get('corp_type')
        self.filing_type_code = kwargs.get('filing_type_code')
        self.jurisdiction = kwargs.get('jurisdiction', None)
        self.date = kwargs.get('date', None)
        self.priority = kwargs.get('priority', None)
        self.headers = kwargs.get('headers', None)


def calculate_fees(req):
    try:
        # Create an instance of the API class
        api_instance = SBCPaymentClient()
        # Calculate Fees
        api_response = api_instance.calculate_fees(
            req.corp_type,
            req.filing_type_code,
            jurisdiction=req.jurisdiction,
            date=req.date,
            priority=req.priority,
            headers=req.headers,
        )

        current_app.logger.debug(api_response)
        return api_response

    except Exception as err:
        raise SBCPaymentException(err)
