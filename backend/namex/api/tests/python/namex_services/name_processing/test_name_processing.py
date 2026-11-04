import pytest

from namex.services.name_request.auto_analyse.protected_name_analysis import ProtectedNameAnalysisService

from ... import integration_synonym_api

service = ProtectedNameAnalysisService()
np_svc = service.name_processing_service


@integration_synonym_api
@pytest.mark.parametrize(
    'name, expected',
    [
        ('ARMSTRONG PLUMBING LTD./ ARMSTRONG PLUMBING LTEE', 'ARMSTRONG PLUMBING'),
        ('VOLVO CARS OF CANADA CORP./LA COMPAGNIE DES AUTOMOBILES VOLVO DU CANADA', 'VOLVO CARS CANADA'),
        ('MEDIA/PROFESSIONAL INSURANCE SERVICES', 'MEDIA PROFESSIONAL INSURANCE SERVICES'),
        ('UNITED WAY OF THE CENTRAL & SOUTH OKANAGAN/SIMILKAMEEN', 'UNITED WAY CENTRAL SOUTH OKANAGAN SIMILKAMEEN'),
        ('TFI TRANSPORT 27, L.P./TRANSPORT TFI 27 S.E.C.', 'TFI TRANSPORT LP TRANSPORT TFI SEC'),
        ('SMITHERS PARENT/SELF ADVOCATE COALITION SOCIETY', 'SMITHERS PARENT SELF ADVOCATE COALITION'),
        ('RAPHA F/A & SAFETY SUPPLY LTD.', 'RAPHA F SAFETY SUPPLY'),
        ('KARSCOT DISTRIBUTORS / FUN ZONE', 'KARSCOT DISTRIBUTORS FUN ZONE'),
        ('MAPLE RIDGE/PITT MEADOWS YOUTH CENTRE SOCIETY', 'MAPLE RIDGE PITT MEADOWS YOUTH CENTRE'),
    ],
)
def test_set_name_remove_french(name, expected):
    np_svc._prepare_data()
    np_svc.set_name(name)
    cleaned_name = np_svc.processed_name.upper()
    assert cleaned_name == expected


@integration_synonym_api
@pytest.mark.parametrize(
    'name, expected',
    [
        ('ARMSTRONG SOCIETE A RESPONSABILITE LIMITEE PLUMBING', 'ARMSTRONG PLUMBING'),
        ('ARMSTRONG L.L.C. PLUMBING', 'ARMSTRONG PLUMBING'),
        ('LAWYERS-BC.COM SERVICES LTD.', 'LAWYERS BC SERVICES'),
        ('THUNDERROAD.ORG INVESTMENTS INC.', 'THUNDERROAD INVESTMENTS'),
        ('ASSOCIATION OF BC SCAFFOLD CONTRACTORS', 'BC SCAFFOLD CONTRACTORS'),
        ('ROUNDHOUSE CO-OPERATIVE HOUSING ASSOCIATION', 'ROUNDHOUSE HOUSING'),
    ],
)
def test_set_name_regex_remove_designations(name, expected):
    np_svc.set_name(name)
    cleaned_name = np_svc.processed_name.upper()
    assert cleaned_name == expected


@integration_synonym_api
@pytest.mark.parametrize(
    'name, expected',
    [
        ('MAPLE BAY PRE-SCHOOL LTD.', 'MAPLE BAY PRESCHOOL'),
        ('NEW SUPER-WAY TELECOM (CANADA) COMPANY LIMITED', 'NEW SUPERWAY TELECOM CANADA'),
        ("CHILDREN'S-HOUSE MONTESSORI PRE-SCHOOL SOCIETY", 'CHILDREN HOUSE MONTESSORI PRESCHOOL'),
        ('SUPER SHAPE STUDIO - W.C. CARMEN', 'SUPERSHAPE STUDIO WC CARMEN'),
        ('RE MAX MOTOR SALES', 'REMAX MOTOR SALES'),
        ('RE/MAX BOB SMITH', 'REMAX BOB SMITH'),
        ('TRADEPRO/PHOENIX ENTERPRISES INC.', 'TRADEPRO PHOENIX ENTERPRISES'),
        ('COAST WIDE HOMECARE/PAINTING NEEDS LTD', 'COAST WIDE HOMECARE PAINTING NEEDS'),
        ('RE-MAX BOB SMITH', 'REMAX BOB SMITH'),
    ],
)
def test_set_name_regex_prefixes(name, expected):
    np_svc.set_name(name)
    cleaned_name = np_svc.processed_name.upper()
    assert cleaned_name == expected


@integration_synonym_api
@pytest.mark.parametrize(
    'name, expected',
    [
        ("BIG MIKE'S FUN FARM INC.", 'BIG MIKE FUN FARM'),
        ('LONDON AIR SERVICES (NO. 8) LIMITED', 'LONDON AIR SERVICES'),
        ('CATHEDRAL (YR 2008) VENTURES', 'CATHEDRAL VENTURES'),
        ('CATHEDRAL (ANYTHING 2008) VENTURES', 'CATHEDRAL VENTURES'),
        ('NO. 295 CATHEDRAL VENTURES', 'CATHEDRAL VENTURES'),
        ('DISCOVERY RESIDENTIAL HOLDINGS (LOT 4)', 'DISCOVERY RESIDENTIAL HOLDINGS'),
        ('RG LOT 3', 'RG'),
        ('BEEDIE CH PROPERTY (LOT 3-22)', 'BEEDIE CH PROPERTY'),
        ('NEIGHBORHOOD OF LOT 152-38 SUN RIVERS OWNER ASSOCIATION', 'NEIGHBORHOOD SUN RIVERS OWNER'),
        ('CRYSTAL LANES (2006)', 'CRYSTAL LANES'),
        ('PJI PIZZA(POCO)', 'PJI PIZZA POCO'),
        ("J.J.'S HARDWOOD FLOORS AND DECORATING", 'JJ HARDWOOD FLOORS DECORATING'),
    ],
)
def test_set_name_regex_numbers_lot(name, expected):
    np_svc.set_name(name)
    cleaned_name = np_svc.processed_name.upper()
    assert cleaned_name == expected


@integration_synonym_api
@pytest.mark.parametrize(
    'name, expected',
    [
        ('JOHNSON & JOHNSON ENGINEERING', 'JOHNSON ENGINEERING'),
        (
            'JOHNSON & JOHNSON-MERCK CONSUMER PHARMACEUTICALS  OF CANADA',
            'JOHNSON MERCK CONSUMER PHARMACEUTICALS CANADA',
        ),
        ('LOCKS LOCKS & LOCKS ENTERPRISE', 'LOCKS ENTERPRISE'),
        ('ROCK ROCK ENTERPRISES', 'ROCK ENTERPRISES'),
        ('JOHNSON/JOHNSON ENGINEERING', 'JOHNSON ENGINEERING'),
        ('ROCK-ROCK ENTERPRISES', 'ROCK ENTERPRISES'),
        ('IBM.IBM ENGINEERING SOLUTIONS', 'IBM ENGINEERING SOLUTIONS'),
        ('J & J SPORTS RENT WEST', 'JJ SPORTS RENT WEST'),
        ('R R SOLUTIONS', 'RR SOLUTIONS'),
        ('BALL & BALLONS ENTERPRISES', 'BALL BALLONS ENTERPRISES'),
    ],
)
def test_set_name_regex_repeated_strings(name, expected):
    np_svc.set_name(name)
    cleaned_name = np_svc.processed_name.upper()
    assert cleaned_name == expected


# Note: Currently failing, regex_keep_together_abv need to include ordinals such as 4th or 3rd
# @pytest.mark.parametrize("name, expected",
#                          [
#                              ("4THGENERATION ENGINEERING", "4TH GENERATION ENGINEERING"),
#                              ("4THOUGHT SOLUTIONS", "4TH OUGHT SOLUTIONS"),
#                              ("3RDEYE SOFTWARE SOLUTIONS", "3RD EYE SOFTWARE SOLUTIONS"),
#                          ]
#                          )
# def test_set_name_regex_separated_ordinals(name, expected):
#     np_svc.set_name(name)
#     cleaned_name = np_svc.processed_name.upper()
#     assert cleaned_name == expected


@integration_synonym_api
@pytest.mark.parametrize(
    'name, expected',
    [
        ('XLR8 ENTERPRISES', 'XLR8 ENTERPRISES'),
        ('ISLAND H20 SERVICES', 'ISLAND H SERVICES'),
        ('GR8 IDEAS MANAGEMENT CONSULTANTS', 'GR8 IDEAS MANAGEMENT CONSULTANTS'),
        ('A1 QUALITY COLLISION SERVICES', 'A1 QUALITY COLLISION SERVICES'),
        ('H20 GROUP SOLUTIONS', 'H GROUP SOLUTIONS'),
        ('G7 INTERNATIONAL GROUP', 'G INTERNATIONAL GROUP'),
    ],
)
def test_set_name_regex_keep_together_abv(name, expected):
    np_svc.set_name(name)
    cleaned_name = np_svc.processed_name.upper()
    assert cleaned_name == expected


@integration_synonym_api
@pytest.mark.parametrize(
    'name, expected',
    [
        ('J & K ENGRAVING', 'JK ENGRAVING'),
        ('D&G WESTCOAST HOMES', 'DG WESTCOAST HOMES'),
        ('DO & BE COLLECTION RETAIL', 'DO COLLECTION RETAIL'),
        ('C & C TRAILER LIFT SYSTEMS', 'CC TRAILER LIFT SYSTEMS'),
        ('C S A DESIGN & DRAFTING SERVICES', 'CS DESIGN DRAFTING SERVICES'),
        ('INTERNATIONAL BUSINESS BUY/SELL', 'INTERNATIONAL BUSINESS BUY SELL'),
        ('GRAHAM/WALL CONSULTING', 'GRAHAM WALL CONSULTING'),
        ('IBI/HB ARCHITECTS', 'IBI HB ARCHITECTS'),
        ('TEANOOK / JOHNSON HOLDINGS', 'TEANOOK JOHNSON HOLDINGS'),
        ('JILLY-BEAN SWEETS & SAVORIES', 'JILLY BEAN SWEETS SAVORIES'),
        ('VIDICO - DATA INTEGRATION', 'VIDICO DATA INTEGRATION'),
        ('KA-CHEE ENTERPRISES', 'KA CHEE ENTERPRISES'),
        ('MR RENT-A-CAR', 'MR RENT CAR'),
    ],
)
def test_set_name_regex_punctuation(name, expected):
    np_svc.set_name(name)
    cleaned_name = np_svc.processed_name.upper()
    assert cleaned_name == expected


@integration_synonym_api
@pytest.mark.parametrize(
    'name, expected',
    [
        ('J K ENGRAVING', 'JK ENGRAVING'),
        ('D G WESTCOAST HOMES', 'DG WESTCOAST HOMES'),
        ('DO BE COLLECTION RETAIL', 'DO COLLECTION RETAIL'),  # --> be is stop words and removed
        ('C C TRAILER LIFT SYSTEMS', 'CC TRAILER LIFT SYSTEMS'),
        ('C S A DESIGN  DRAFTING SERVICES', 'CS DESIGN DRAFTING SERVICES'),
        ('DG ART DESIGN  DRAFTING SERVICES', 'DG ART DESIGN DRAFTING SERVICES'),
    ],
)
def test_set_name_regex_together_one_letter(name, expected):
    np_svc.set_name(name)
    cleaned_name = np_svc.processed_name.upper()
    assert cleaned_name == expected


@integration_synonym_api
@pytest.mark.parametrize(
    'name, expected',
    [
        ('KOINZ 4 KIDZ SOCIETY', 'KOINZ KIDZ'),
        ('KLEYSEN GROUP 2006', 'KLEYSEN GROUP'),
        ('KANCO 1323 WEST 71ST APARTMENTS', 'KANCO WEST APARTMENTS'),
        ('GAM SHOES REPAIR #3', 'GAM SHOES REPAIR'),
    ],
)
def test_set_name_regex_strip_out_numbers_middle_end(name, expected):
    np_svc.set_name(name)
    cleaned_name = np_svc.processed_name.upper()
    assert cleaned_name == expected


@integration_synonym_api
@pytest.mark.parametrize(
    'name, expected',
    [
        ('654101 BC LTD.', '654101 BC'),
        ('7308 HOLDINGS LTD.', '7308 HOLDINGS'),
        ('13192427 ENTERPRISES INC.', '13192427 ENTERPRISES'),
        ('1984 VENTURES LTD.', '1984 VENTURES'),
        ('KKBL NO. 546 VENTURES LTD.', 'KKBL VENTURES'),
        ('2020 SOLUTIONS LTD.', '2020 SOLUTIONS'),
        ('1900 INDUSTRIES INC.', '1900 INDUSTRIES'),
        ('947 FORT HOLDINGS LTD.', 'FORT HOLDINGS'),
        ('200 INTERCHANGE VENTURES LLP', 'INTERCHANGE VENTURES'),
        ('588618 BRITISH COLUMBIA LTD.', '588618 BRITISH COLUMBIA'),
        ('1198430 ALBERTA LTD.', '1198430 ALBERTA'),
        ('2705 INVESTMENTS LTD.', '2705 INVESTMENTS'),
        ('4936290 MANITOBA LTD.', '4936290 MANITOBA'),
        ('1091064 ONTARIO LIMITED', '1091064 ONTARIO'),
        ('3120579 NOVA SCOTIA LTD.', '3120579 NOVA SCOTIA'),
    ],
)
def test_set_name_keep_numbers_beginning(name, expected):
    np_svc.set_name(name)
    cleaned_name = np_svc.processed_name.upper()
    assert cleaned_name == expected
