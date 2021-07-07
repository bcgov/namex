from datetime import date


def build_payment_request(nr_model):
    """
    Builds a payment request object using a supplied Request (nr_model) model.
    :param nr_model:
    :return:
    """
    nr_name = nr_model.names[0]
    nr_applicant = nr_model.applicants[0]

    if not nr_name and nr_applicant:
        raise Exception('Cannot build payment request, please supply an NR with a name and an applicant defined!')

    payment_request = {
        # Comment this out to use direct pay
        # 'paymentInfo': {
        #     'methodOfPayment': 'CC',
        # },
        'filingInfo': {
            'date': date.today(),
            'filingTypes': [
                {
                    'filingDescription': '',  # 'NM620: ' + nr_name.name,
                    'filingTypeCode': 'NM620',  # TODO: Use an enum
                    'priority': (nr_model.priorityCd == 'Y')  # TODO: Use an enum
                }
            ],
        },
        'businessInfo': {
            'corpType': 'NRO',
            'businessIdentifier': nr_model.nrNum,
            'businessName': nr_name.name,
            'contactInfo': {
                # TODO: Concat this for payments?
                # 'addressLine1': ', '.join([nr_applicant.addrLine1, nr_applicant.addrLine2]),
                'addressLine1': nr_applicant.addrLine1,
                'city': nr_applicant.city,
                'province': nr_applicant.stateProvinceCd,
                'country': nr_applicant.countryTypeCd,
                'postalCode': nr_applicant.postalCd
            }
        },
        'details': build_payment_details(nr_model)
    }

    return payment_request


def merge_payment_request(nr_model, config=None):
    """
    Builds a custom payment request object using a supplied Request (nr_model) model and a dict of overrides.
    :param nr_model: The Name Request (Request) model.
    :param config: An optional dictionary of overrides.
    :return:
    """
    nr_name = nr_model.names[0]
    nr_applicant = nr_model.applicants[0]

    # TODO: This isn't robust enough!
    if not config and (not nr_name or not nr_applicant):
        raise Exception('Cannot build payment request, please supply an NR with a name and an applicant defined!')

    # Comment out to use direct pay
    # method_of_payment = 'CC'

    filing_date = date.today()
    filing_description = ''
    filing_type_code = ''  # TODO: Use an enum
    priority_request = (nr_model.priorityCd == 'Y')  # TODO: Use an enum

    corp_type = 'NRO'
    business_id = nr_model.nrNum
    business_name = nr_name.name

    address_line_1 = nr_applicant.addrLine1
    city = nr_applicant.city
    province = nr_applicant.stateProvinceCd
    country = nr_applicant.countryTypeCd
    postal_code = nr_applicant.postalCd

    # If contact info is supplied use the ENTIRE contactInfo
    if isinstance(config, dict):
        payment_info_config = config.get('paymentInfo')
        # Comment out to use direct pay
        # if payment_info_config:
        #     method_of_payment = payment_info_config.get('methodOfPayment', method_of_payment)

        filing_info_config = config.get('filingInfo')
        if filing_info_config:
            filing_date = filing_info_config.get('date', filing_date)

            # TODO: To support more than one filing type at once this would need to be updated
            #  Right now, we only use one. so this is fine as is
            filing_types = filing_info_config.get('filingTypes')[0] \
                if isinstance(filing_info_config.get('filingTypes'), list) and filing_info_config.get('filingTypes')[0] else None
            if filing_types and isinstance(filing_types, dict):
                filing_description = filing_types.get('filingDescription', filing_description)
                filing_type_code = filing_types.get('filingTypeCode', filing_type_code)
                priority_request = filing_types.get('priority', priority_request)

        business_info_config = config.get('businessInfo')
        if business_info_config:
            corp_type = business_info_config.get('corpType', corp_type)
            business_id = business_info_config.get('businessIdentifier', business_id)
            business_name = business_info_config.get('businessName', business_name)

            contact_info = business_info_config.get('contactInfo')
            if contact_info and isinstance(contact_info, dict):
                address_line_1 = contact_info.get('addressLine1', address_line_1)
                city = contact_info.get('city', city)
                province = contact_info.get('province', province)
                country = contact_info.get('country', country)
                postal_code = contact_info.get('postalCode', postal_code)

    payment_request = {
        # 'paymentInfo': {
        #     'methodOfPayment': method_of_payment,
        # },
        'filingInfo': {
            'date': filing_date,
            'filingTypes': [
                {
                    # Exclude filing description
                    # 'filingDescription': filing_description,
                    'filingTypeCode': filing_type_code,
                    'priority': priority_request
                }
            ],
        },
        'businessInfo': {
            'corpType': corp_type,
            'businessIdentifier': business_id,
            'businessName': business_name,
            'contactInfo': {
                'addressLine1': address_line_1,
                'city': city,
                'province': province,
                'country': country,
                'postalCode': postal_code
            }
        },
        'details': build_payment_details(nr_model)
    }

    return payment_request

def build_payment_details(nr_model):
    """Build payment details."""
    details = []
    details.append(
        {
            'label': 'NR Number:',
            'value': nr_model.nrNum
        }
    )
    details.append(
        {
            'label': 'Name Choices:',
            'value': ''
        }
    )
    name_choices = sorted(nr_model.names.all(), key=lambda x: x.choice)
    for name in name_choices:
        details.append(
            {
                'label': str(name.choice) + '.',
                'value': name.name
            }
        )

    return details