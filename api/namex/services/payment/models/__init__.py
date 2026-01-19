from dataclasses import dataclass, field
from typing import Optional, Union
from decimal import Decimal

from pydantic.dataclasses import dataclass as pydantic_dataclass
from pydantic import Field
from datetime import date

from .abstract import Serializable


@dataclass
class PaymentInfo(Serializable):
    methodOfPayment: str


@dataclass
class FilingInfo(Serializable):
    corpType: str
    date: date
    filingTypes: list


@dataclass
class FilingType(Serializable):
    filingTypeCode: str
    priority: str
    filingTypeDescription: str


@dataclass
class ContactInfo(Serializable):
    firstName: str
    lastName: str
    address: str
    city: str
    province: str
    postalCode: str


@dataclass
class BusinessInfo(Serializable):
    businessIdentifier: str
    businessName: str
    contactInfo: ContactInfo


@dataclass
class AccountInfo(Serializable):
    routingSlip: str
    bcolAccountNumber: str
    datNumber: str


@dataclass
class PaymentDetailItem:
    label: str
    value: str


@dataclass
class PaymentRequest(Serializable):
    """
    Sample request:
    {
        "paymentInfo": {
            "methodOfPayment": "CC"
        },
        "businessInfo": {
            "businessIdentifier": "CP1234567",
            "corpType": "NRO",
            "businessName": "ABC Corp",
            "contactInfo": {
                "city": "Victoria",
                "postalCode": "V8P2P2",
                "province": "BC",
                "addressLine1": "100 Douglas Street",
                "country": "CA"
            }
        },
        "filingInfo": {
            "filingTypes": [
                {
                    "filingTypeCode": "ABC",
                    "filingDescription": "TEST"
                },
                {
                    "filingTypeCode": "ABC"
                    ...
                }
            ]
        },
        "details": [
            {
                "label": 'NR Number:',
                "value": 'NR 1234567'
            },
            {
                "label": 'Name Choices:',
                "value": ''
            },
            {
                "label": '1.',
                "value": 'CINEXTREME LEGAL SERVICES LIMITED'
            },
            {
                "label": '2.',
                "value": 'BRUNETTE HUNTING AND TRAPPING LIMITED'
            },
            {
                "label": '3.',
                "value": 'ALKEM CLOTHING STORES LIMITED'
            }
        ]
    }
    """

    paymentInfo: PaymentInfo
    filingInfo: FilingInfo
    businessInfo: BusinessInfo
    accountInfo: AccountInfo
    details: list = field(default_factory=PaymentDetailItem)


class PydanticConfig:
    """Pydantic config to ignore extra fields."""
    extra = 'ignore'
    underscore_attrs_are_private = False


@pydantic_dataclass(config=PydanticConfig)
class PaymentRefundInvoice:
    refundId: int
    refundAmount: Decimal
    message: str
    isPartialRefund: bool


@pydantic_dataclass(config=PydanticConfig)
class PaymentInvoice(Serializable):
    id: int
    serviceFees: float
    paid: float
    refund: float
    total: float
    bcolAccount: int = None
    isPaymentActionRequired: bool = field(default_factory=bool)
    statusCode: str = ''
    createdBy: str = ''
    createdName: str = ''
    createdOn: str = ''
    updatedBy: str = ''
    updatedName: str = ''
    updatedOn: str = ''
    paymentMethod: str = ''
    businessIdentifier: str = ''
    corpTypeCode: str = ''
    routingSlip: str = ''
    datNumber: str = ''
    folioNumber: str = ''
    lineItems: list = Field(default_factory=list)
    receipts: list = Field(default_factory=list)
    references: list = Field(default_factory=list)
    details: list = Field(default_factory=list)
    links: list = Field(default_factory=list)
    paymentAccount: dict = Field(default_factory=dict)

    @property
    def _links(self) -> list:
        return self.links

    @_links.setter
    def _links(self, value: list) -> None:
        self.links = value


@dataclass
class ReceiptRequest(Serializable):
    corpName: str = ''
    companyActDetails: str = ''
    businessNumber: str = ''
    recognitionDateTime: str = ''
    filingIdentifier: str = ''
    filingDateTime: str = ''
    fileName: str = ''


@dataclass
class Receipt(Serializable):
    id: int
    receiptAmount: float
    receiptDate: str = ''
    receiptNumber: str = ''


@pydantic_dataclass(config=PydanticConfig)
class ReceiptResponse(Serializable):
    bcOnlineAccountNumber: Optional[str] = None
    filingIdentifier: Optional[str] = None
    invoice: Optional[Union[PaymentInvoice, dict]] = None
    invoiceNumber: str = ''
    paymentMethod: str = ''
    receiptNumber: str = ''
    routingSlipNumber: str = ''
