import dataclasses

from dataclasses import dataclass, field
from pydantic.dataclasses import dataclasses as pydantic_dataclass
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


@dataclass
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
    lineItems: list = field(default_factory=list)
    receipts: list = field(default_factory=list)
    references: list = field(default_factory=list)
    details: list = field(default_factory=list)
    _links: list = field(default_factory=list)
    paymentAccount: dict = field(default_factory=dict)

    def __init__(self, **kwargs):
        """Set the attributes only if the field is defined."""
        self.lineItems = []
        self.receipts = []
        self.references = []
        self.details = []
        self._links = []
        self.paymentAccount = {}
        names = {f.name for f in dataclasses.fields(self)}
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


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


class PydanticConfig:
    """Pydantic config to ignore extra fields."""
    extra = 'ignore'


@pydantic_dataclass(config=PydanticConfig)
class ReceiptResponse(Serializable):
    bcOnlineAccountNumber: str = None
    filingIdentifier: str = None
    invoice: PaymentInvoice = field(default=PaymentInvoice)
    invoiceNumber: str = ''
    paymentMethod: str = ''
    receiptNumber: str = ''
    routingSlipNumber: str = ''
