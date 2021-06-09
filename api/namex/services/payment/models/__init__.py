from .abstract import Serializable
from dataclasses import dataclass, field
from datetime import date


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
        }
    }
    """
    paymentInfo: PaymentInfo
    filingInfo: FilingInfo
    businessInfo: BusinessInfo
    accountInfo: AccountInfo


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


@dataclass
class ReceiptResponse(Serializable):
    bcOnlineAccountNumber: str = None
    filingIdentifier: str = None
    invoice: PaymentInvoice = field(default=PaymentInvoice)
    invoiceNumber: str = ''
    paymentMethod: str = ''
    receiptNumber: str = ''
    routingSlipNumber: str = ''
