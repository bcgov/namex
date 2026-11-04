export enum PaymentMethod {
    DIRECT_PAY = 'DIRECT_PAY', // Credit Card
    INTERNAL = 'INTERNAL', // Staff payment: Routing Slip and No Fee
    DRAWDOWN = 'DRAWDOWN', // BCOL
    PAD = 'PAD', // Premiun Authorized Debit

    // Not used by Name Request atm
    CC = 'CC', // Credit Card
    EFT = 'EFT', // Eletronic Funds Transfer
    WIRE = 'WIRE', // Wire Transfer
    ONLINE_BANKING = 'ONLINE_BANKING', // Online Banking
    EJV = 'EJV' // Electronic Journal Voucher
}
