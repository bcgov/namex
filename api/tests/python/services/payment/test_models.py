# Copyright © c2021 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from namex.services.payment.models import PaymentInvoice


def test_payment_invoice_model(session):
    """Assert that the data class ignores unknown response attributes."""
    sample_response = {
        'businessIdentifier': 'NR L000002',
        'corpTypeCode': 'NRO',
        'id': 11801,
        'paid': 0.0,
        'paymentAccount': {
            'accountId': '2698',
            'accountName': 'online banking 13.1'
        },
        'paymentMethod': 'ONLINE_BANKING',
        'serviceFees': 1.5,
        'statusCode': 'CREATED',
        'total': 31.5,
        'test_field_to_be_ignored': 'Hi'
    }

    invoice_model = PaymentInvoice(**sample_response)
    assert invoice_model.businessIdentifier == sample_response['businessIdentifier']
    assert not getattr(invoice_model, 'test_field_to_be_ignored', None)
    assert invoice_model.lineItems == []
    assert invoice_model.receipts == []
    assert invoice_model.references == []
    assert invoice_model._links == []

