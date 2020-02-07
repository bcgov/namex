from namex.services.name_request.auto_analyse.name_analysis_utils import \
    data_frame_to_list, clean_name_words, regex_transform, remove_french, get_substitution_list, get_stop_word_list, \
    get_prefix_list, get_fr_designation_end_list, \
    get_stand_alone_list, get_words_to_avoid, is_substitution_word, get_classification, get_list_of_lists, \
    get_words_requiring_consent, get_designations_in_name, get_en_designation_any_all_list, \
    get_en_designation_end_all_list, get_designation_by_entity_type

from hamcrest import *
import pandas as pd

text = 'WM H20 VENTURES INC'
# text = 'W & M MOUNTAIN VENTURES INC.'
word = 'MOUNTAIN'

name = ['WM', 'MOUNTAIN', 'VENTURES']

substitution_word = '4mula'
list_dist = []
list_desc = []
list_none = ['MOUNTAIN', 'VIEW', 'FOOD', 'GROWERS']

name = ['WM', 'MOUNTAIN', 'VENTURES']

substitution_word = '4mula'
list_dist = ['WM', '4BY4']
list_desc = ['VENTURES']
list_none = []

name = ['WM', 'MOUNTAIN', 'VENTURES']

substitution_word = '4mula'
list_dist = ['WM', '4BY4']
list_desc = ['VENTURES']
list_none = []

stop_words = ['an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', \
              'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 'on', 'or', \
              'such', 'that', 'the', 'their', 'then', 'there', 'these', \
              'they', 'this', 'to']
en_designation_any_list = ['association', 'assoc', 'assoc.', 'assn', 'assn.', 'society', 'soc', \
                           'soc.', 'foundation', 'co-operative', 'co-op', 'coop', 'cooperative']

en_designation_end_list = ['llc', 'l.l.c', 'limited liability company', 'llp', 'limited liability partnership', \
                           'limited partnership', 'limited', 'ltd', 'ltd.', 'incorporated', 'inc', 'inc.', \
                           'corporation', 'corp', 'corp.', 'ulc.', 'ulc', 'unlimited liability company', \
                           'company', 'co', 'co.', 'liability']

fr_designation_end_list = ['ltee', 'ltee.', 'incorporee', ' societe a responsabilite limitee', \
                           'societe en nom collectif a responsabilite limitee', 'slr', 'sencrl', \
                           'limitee', 'incorporee']

stand_alone_list = ['bc', 'holdings', 'ventures', 'solutions', 'enterprise', 'industries']

prefix_list = ['un', 're', 'in', 'dis', 'en', 'non', 'in', 'over', 'mis', 'sub', 'pre', 'inter', 'fore', 'de', 'trans', \
               'super', 'semi', 'anti', 'mid', 'under', 'ante', 'bene', 'circum', 'co', 'com', 'con', 'col', 'dia', \
               'ex', 'homo', 'hyper', 'mal', 'micro', 'multi', 'para', 'poly', 'post', 'pro', 'retro', 'tele', \
               'therm', 'trans', 'uni']

words_to_avoid = ['FOLLOW THE BIRDS TO VICTORIA', 'FARMERS INSTITUTE', 'VSE', 'PIC A FLIC', 'PICK A FLIC',
                  'PICK A FLICK', 'PIK A FLIC', 'CPIC', 'CANADIAN NATIONAL', 'CN', 'GRAND TRUNK', 'POST OFFICE',
                  'POSTAL', 'KKK',
                  'KLU KLUX KLAN', 'NATIONALIST PARTY OF CANADA', 'ICPO', 'INTERPOL', 'GST', 'BC TECH', 'BC TECHNOLOG',
                  'BCTEC',
                  'BCTECH', 'BC TEK', 'BCTEK', 'CANADA STANDARD', 'R C M P', 'RCMP', 'ROYAL CANADIAN MOUNTED POLICE',
                  'SAVINGS AND LOAN',
                  'CREDIT UNION', 'CU', 'BANKRUPT', 'BANKRUPTCY', 'BBB', 'BETTER BUSINESS BUREAU', 'LLB',
                  'KNIGHTS OF MALTA', 'ORDER OF MALTA', 'COUNTY COURT', 'PROVINCIAL COURT', 'SUPREME COURT', 'BUILD BC',
                  'ANIMAL CRUELTY',
                  'CRUELTY TO ANIMALS', 'SPCA', 'BONDED', 'CERTIFIED', 'CERTIFY', 'GUARANTEE', 'GUARANTEED', 'LICENCED',
                  'LICENSED', 'QUALIFIED', 'BC ONLINE', 'BCONLINE', 'BISHOP ALEXANDER CARTER CHARITABLE FUND',
                  'ACCESS BC', 'ACCESSBC', 'RD STAR', 'ROAD STAR', 'ROADSTAR', 'AUTHORIZED', '211 BC', '211 SERVICES',
                  '211 SOCIETY', 'BC 211', 'ABSTRACT', 'WHITE KNIGHT']

words_require_consent = ['CGA', 'COLIN LIAM BEECHINOR', 'COLIN SMILE', 'COLINS SMILE', '4 H', '4H', 'SUMMER GAMES',
                         'WINTER GAMES', 'HOMALCO', 'HONEYWELL', 'HBC', 'HUDSONS BAY COMPANY', 'BUICK', 'CHEVROLET',
                         'GEO', 'ISUZU', 'OLDSMOBILE', 'PONTIAC', 'SATURN', 'INTERMEDIATE CARE', 'LEGION',
                         'ROYAL CANADIAN LEGION', 'MACK TRUCK', 'MACK TRUCKS', 'MULTIPLE LISTING SERVICE', 'CRIME',
                         'CRIME STOPPER', 'CRIME STOPPERS', 'CRIMESTOPPER', 'CROOKSTOPPER', 'LAW ENFORCEMENT',
                         'NEIGHBORHOOD WATCH', 'NEIGHBOURHOOD WATCH', 'CERTIFIED MANAGEMENT CONSULTANT', 'CMC', 'CPRPM',
                         'REGISTERED CERTIFIED PROFESSIONAL RESIDENTIAL PROPERTY MANAG', 'REG OT BC',
                         'REGISTERED OCCUPATIONAL THERAPISTS BC', 'EMILY CARR', 'REGISTERED INTERIOR DESIGNER', 'RID',
                         'RID CHARTER', 'RID FELLOW', 'RI BC', 'REGISTERED PLANNER', 'COMMONWEALTH SOCIETY',
                         'REGISTERED ENVIRONMENTAL HEALTH OFFICER', 'REGISTERED PUBLIC HEALTH INSPECTOR', 'REHO',
                         'RPHI', 'LABRADOR', 'NEWFOUNDLAND', 'NORTHWEST TERRITORITIES', 'NUNAVUT', 'NWT',
                         'REGISTERED AUDIOLOGIST', 'REGISTERED COMMUNICATION DISORDERS SPECIALIST',
                         'REGISTERED SPEECH LANGUAGE PATHOLOGIST', 'REGISTERED SPEECH LANGUAGE THERAPIST',
                         'REGISTERED SPEECH PATHOLOGIST', 'REGISTERED SPEECH THERAPIST', 'REGISTERED VOICE THERAPIST',
                         'REGISTERED INDUSTRIAL ACCOUNTANT', 'RIA', 'LANDSCAPE ARCHITECT', 'LANDSCAPE ARCHITECTS',
                         'LANDSCAPE ARCHITECTURE', 'REGISTERED MUSIC TEACHER', 'RMT', 'MASSAGE PRACTITIONER',
                         'MASSAGE THERAPIST', 'MASSAGE THERAPY', 'REGISTERED MASSAGE PRACTICE',
                         'REGISTERED MASSAGE PRACTITIONER', 'REGISTERED MASSAGE THERAPIST',
                         'REGISTERED MASSAGE THERAPY', 'THERAPEUTIC MASSAGE', 'REGISTERED SOCIAL WORKER',
                         'REGISTERED SOCIAL WORKERS', 'RSW', 'SOCIAL WORKER', 'ANIMAL CLINIC', 'ANIMAL HOSPITAL',
                         'D V M', 'DVM', 'PET HOSPITAL', 'VETERINARIAN', 'VETERINARIANS', 'VETERINARY', 'KHOWUTZUN',
                         'ORANGE LODGE', 'ORANGE LODGES', 'TAHLTAN', 'GP', 'CITIZENS ADVOCACY', 'THE MORTGAGE CENTRE',
                         'COMMONWEALTH', 'LICENSED PRACTICAL NURSE', 'LPN', 'DRUGLESS HEALER', 'DRUGLESS PHYSICIAN',
                         'NATURAL MEDICINE', 'NATUROPATH', 'NATUROPATHIC', 'NATUROPATHIC MEDICINE',
                         'NATUROPATHIC PHYSICIAN', 'SANIPRACTIC', 'naturopathicdoctor',
                         'REGISTERED PROFESSIONAL BIOLOGIST', 'RP BIO', 'BC HYDRO', 'C N R', 'C P R', 'CBC', 'CNR',
                         'CPR', 'ECM', 'EUROPEAN COMMON MARKET', 'JAYCEE', 'PORT OF PRINCE RUPERT', 'PORT OF VANCOUVER',
                         'VANCOUVER PORT', 'REGIONAL BOARD', 'REGIONAL DISTRICT', 'COLDWELL BANKER', 'LIONESS', 'LIONS',
                         'LIONS CLUB', 'KIWANIS', 'CERTIFIED MANAGEMENT ACCOUNTANT', 'CMA', 'MAZDA', 'TOYOTA',
                         'BARRISTER', 'LAW', 'LAW CORPORATION', 'LAWYER', 'LAWYERS', 'PERSONAL LAW', 'SOLICITOR',
                         'SOLICITORS', 'BCLS', 'LAND SURVEY', 'LAND SURVEYING', 'LAND SURVEYOR', 'LAND SURVEYORS',
                         'LAND SURVEYS', 'PLS', 'ROTARACT', 'ROTARY', 'THE BODY SHOP', 'SHINING LIGHT',
                         'THE SHINING LIGHT', 'KIN', 'KINETTE', 'KINSMEN', 'NISSAN', 'LADA', 'BARRISTERS', 'UNBC',
                         'UNIVERSITY OF NORTHERN BRITISH COLUMBIA', 'HYUNDAI', 'ALBERTA', 'MANITOBA', 'NEW BRUNSWICK',
                         'NOVA SCOTIA', 'ONTARIO', 'PRINCE EDWARD ISLAND', 'CASINO', 'CASINOS', 'LOTO', 'LOTTERIES',
                         'LOTTERY', 'LOTTO', 'LTC', 'SLOT', 'ASSURANCE', 'DEPOSIT', 'INDEMNITY', 'INSURANCE',
                         'REINSURANCE', 'SURETY', 'UNDERWRITING', 'IMASCO', 'OPTIMIST', 'QUENEESH', 'R H I',
                         'REGISTERED HOME INSPECTOR', 'RHI', 'REALTY EXECUTIVES', 'SUBARU', 'CARLSON WAGONLIT', 'AIBC',
                         'ARCH', 'ARCHITECT', 'ARCHITECTS', 'ARCHITECTURAL', 'ARCHITECTURE', 'BC GETAWAYS',
                         'CANADAS WEST', 'SUPER NATURAL', 'SUPERHOST', 'UNIVERSITY OF VICTORIA', 'UVIC',
                         'MACDONALD REALT', 'REGISTERED PROFESSIONAL CONSULTING ARCHAEOLOGIST', 'RPCA', 'I P A',
                         'I S P', 'INFORMATICIEN PROFESSIONNEL AGREE DU CANADA',
                         'INFORMATION SYSTEMS PROFESSIONAL OF CANADA', 'IPA', 'ISP', 'BINGO', 'GAMBLE', 'GAMBLING',
                         'GAMING', 'RACINO', 'RAFFLE', 'SLOTS', 'REGISTERED SHIATSU THERAPIST', 'RST',
                         'CERTIFIED FINANCIAL PLANNER', 'CFP', 'DENTAL MECHANIC', 'DENTURE', 'DENTURES', 'DENTURIST',
                         'COQUIHALLA HIGHWAY', 'BC BAR', 'BRITISH COLUMBIA BAR', 'BRITISH COLUMBIA BAR ASSOCIATION',
                         'THE BRITISH COLUMBIA BAR ASSOCIATION', 'DENTAL HYGIENE', 'DENTAL HYGIENIST', 'RDH', 'LEGAL',
                         'LEGAL SERVICE', 'LEGAL SERVICES', 'LEGALSERVICE', 'LEGALSERVICES', 'BVMS', 'PET CLINIC',
                         'VET', 'BIKRAM', 'BIKRAMS', 'HOSPITALIST', 'HOSPITALISTS', 'OCCUPATIONAL THERAPIST',
                         'OCCUPATIONAL THERAPISTS', 'OCCUPATIONAL THERAPY', 'CONTACT LENS FITTER',
                         'CONTACT LENS FITTERS', 'DISPENSING OPTICIAN', 'DISPENSING OPTICIANS', 'OPTICIAN', 'OPTICIANS',
                         'ACUPUNCTURE', 'ACUPUNCTURIST', 'ACUPUNCTURISTS', 'CHINESE MEDICINE',
                         'DOCTOR OF TRADITIONAL CHINESE MEDICINE', 'TCM', 'TRADITIONAL CHINESE MEDICINE HERBALIST',
                         'TRADITIONAL CHINESE MEDICINE PRACTITIONER', 'AUDIOLOGIST', 'AUDIOLOGY', 'AUDIOMETRIC',
                         'AUDIOMETRY', 'HEARING AID', 'HEARING INSTRUMENT PRACTITIONER', 'SPEECH', 'SPEECH LANGUAGE',
                         'EMERGENCY MEDICAL ASSISTANT', 'MIDWIFE', 'MIDWIFERY', 'MIDWIFES', 'MIDWIVE', 'MIDWIVES',
                         'LEGAL EASE', 'LEGALEASE', 'DOCTOR OF PODIATRIC MEDICINE', 'PODIATRIC', 'PODIATRIC DOCTOR',
                         'PODIATRIC DR', 'PODIATRIST', 'PODIATRISTS', 'PODIATRY', 'UNDERWRITERS', 'HONDA', 'ASSURANCES',
                         'ASSURE', 'CASUALTY', 'INSURER', 'INSURERS', 'LIABILITY', 'REINSURE', 'REINSURER', 'ASSURANT',
                         'ASSUREUR', 'DASSURANCES', 'DE FIDUCIE', 'FIDUCIARE', 'UNDERWRITER', 'WARRANTIES', 'WARRANTY',
                         'FIDUCIE', 'GARANTIE', 'INDEMNITE', 'LASSURANCE', 'LASSUREUR', 'REASSURANCE', 'REASSURANCES',
                         'SOUSCRIPTION', 'SOUSCRIRE', 'SUCSRIPTEUR', 'SURETE', 'DENTISTS', 'REALTOR', 'REALTORS',
                         'BC ROYAL', 'ROYAL BC', 'ROYAL CANADIAN', 'DOMINION LENDING CENTRE',
                         'DOMINION LENDING CENTRES', 'SPEECHLANGUAGE', 'NOTARIAL', 'NOTARIES', 'NOTARIES PUBLIC',
                         'NOTARY', 'NOTARY PUBLIC', 'GEOLOGY', 'GEOMORPHOLOGY', 'GEOPHYSICAL', 'GEOPHYSICS',
                         'GEOSCIENCE', 'HYDROGEOLOGY', 'PETROLEUM GEOSCIENCE', 'QUATERNARY GEOLOGY', 'GEOLOGICAL',
                         'GEOLOGIST', 'GEOSCIENTIST', 'UCLUELET FIRST NATION', 'ULKATCHO', 'UNION BAR FIRST NATION',
                         'UPPER NICOLA', 'UPPER SIMILKAMEEN', 'WEST MOBERLY FIRST NATIONS', 'WESTBANK FIRST NATION',
                         "WET'SUWET'EN FIRST NATION", 'WHISPERING PINES/CLINTON', 'WILLIAMS LAKE',
                         'WITSET FIRST NATION', 'YMCA', 'YMCAYWCA', 'YMYWCA', 'YWCA', 'WUIKINUXV NATION', "XAXLI'P",
                         "XENI GWET'IN FIRST NATIONS GOVERNMENT", 'YAKWEAKWIOOSE', 'YALE FIRST NATION',
                         'YEKOOCHE FIRST NATION', "YUNESIT'IN GOVERNMENT", "TL'AZT'EN NATION", "TL'ETINQOX GOVERNMENT",
                         "TLA'AMIN NATION", 'TLA-O-QUI-AHT FIRST NATIONS', 'TLATLASIKWALA', 'TLOWITSIS TRIBE', 'COSTCO',
                         'TOBACCO PLAINS', 'TOOSEY', 'TOQUAHT', "TS'KW'AYLAXW FIRST NATION", "TSAL'ALH", 'TSARTLIP',
                         'TSAWOUT FIRST NATION', 'TSAWWASSEN FIRST NATION', 'TSAY KEH DENE', 'TSESHAHT', 'TSEYCUM',
                         'TSLEIL-WAUTUTH NATION', 'TZEACHTEN', 'UCHUCKLESAHT', 'SKWAH', 'SNUNEYMUXW FIRST NATION',
                         'SODA CREEK', 'SONGHEES NATION', 'SOOWAHLIE', 'SPLATSIN', 'SPUZZUM', 'OPTOMETRIC',
                         'OPTOMETRIC CORPORATION', 'OPTOMETRIST', 'OPTOMETRISTS', 'OPTOMETRY', "SQ'ï¿½ï¿½_WLETS",
                         "SQ'EWLETS", 'SQUAMISH', 'SQUIALA FIRST NATION', "STELLAT'EN FIRST NATION", "STS'AILES",
                         "STSWECEM'C XGAT'TEM FIRST NATION", "STZ'UMINUS FIRST NATION", 'SUMAS FIRST NATION',
                         "T'SOU-KE FIRST NATION", "T'IT'Q'ET", 'TAHLTAN', 'OD FELLOW', 'OD FELOW', 'ODD FELLOW',
                         'ODD FELOW', 'ODFELOW', 'TAKLA LAKE FIRST NATION', "TK'EMLï¿½ï¿½_PS TE SECWï¿½ï¿½_PEMC",
                         "TK'EMLUPS TE SECWEPEMC", 'QUATSINO', "SAIK'UZ FIRST NATION", 'SAMAHQUAM',
                         'SAULTEAU FIRST NATIONS', 'SEABIRD ISLAND', 'SECHELT', 'SEMIAHMOO', 'SHACKAN', 'SHUSWAP',
                         'PAUQUACHIN', 'ASUNA', 'CADILLAC', 'CHEV', 'GM', 'GMC', "SHXW'OW'HAMEL FIRST NATION",
                         "SHXWHï¿½ï¿½_:Y VILLAGE", 'SKWAY FIRST NATION', 'SIMPCW FIRST NATION', 'SISKA',
                         'SKATIN NATIONS', 'SKAWAHLOOK FIRST NATION', 'SKEETCHESTN', 'SKIDEGATE', 'SKIN TYEE',
                         'SKOWKALE', 'SKUPPAH', 'PSYCHOLOGICAL', 'PSYCHOLOGICAL ASSOCIATE', 'PSYCHOLOGIST',
                         'PSYCHOLOGISTS', 'PSYCHOLOGY', 'REGISTERED PSYCHOLOGICAL ASSOCIATE', 'REGISTERED PSYCHOLOGIST',
                         'NICOMEN', "NISGA'A VILLAGE OF GINGOLX", "NISGA'A VILLAGE OF GITWINKSIHLKW",
                         "NISGA'A VILLAGE OF LAXGALT'SAP", "NISGA'A VILLAGE OF NEW AIYANSH", 'NOOAITCH', 'NUCHATLAHT',
                         'NUXALK NATION', 'OKANAGAN', 'OLD MASSETT VILLAGE COUNCIL', 'OREGON JACK CREEK',
                         'ROBERTS BANK', 'OSOYOOS', 'PACHEEDAHT FIRST NATION', 'PAUQUACHIN', 'PENELAKUT TRIBE',
                         'PENTICTON', 'POPKUM', 'PROPHET RIVER FIRST NATION', 'QUALICUM FIRST NATION', 'LOWER NICOLA',
                         'LOWER SIMILKAMEEN', 'LYACKSON', 'LYTTON', 'MALAHAT FIRST NATION',
                         'MAMALILIKULLA FIRST NATION', 'MATSQUI', 'MCLEOD LAKE', 'METLAKATLA FIRST NATION',
                         'MOWACHAHT/MUCHALAHT', 'MUSQUEAM', "N'QUATQUA", 'NADLEH WHUTEN', 'INSURANCES', 'TRUSCO',
                         'TRUST', 'TRUSTCO', 'TRUSTEE', 'TRUSTEES', 'TRUSTS', 'TRUSTY', "NAK'AZDLI WHUT'EN",
                         'NAMGIS FIRST NATION', 'NANOOSE FIRST NATION', 'NAZKO FIRST NATION', 'NEE-TAHI-BUHN',
                         'NESKONLITH', 'NEW WESTMINSTER', 'KITSELAS', 'KITSUMKALUM', 'KLAHOOSE FIRST NATION',
                         'KWADACHA', 'VOLKS', 'VOLKSWAGEN', 'KWAKIUTL', 'KWANTLEN FIRST NATION', 'KWAW-KWAW-APILT',
                         'KWIAKAH', "KWIKWASUT'INUXW HAXWA'MIS", 'KWIKWETLEM FIRST NATION', 'LAKE BABINE NATION',
                         'LAKE COWICHAN FIRST NATION', "LAX KW'ALAAMS", 'KIA', "LEQ' A: MEL FIRST NATION",
                         "LHEIDLI T'ENNEH", 'COMMUNITY CHEST', 'UNITED WAY', 'WESTAR', "LHOOSK'UZ DENE NATION",
                         'LHTAKO DENE NATION', "LIL'WAT NATION", 'LITTLE SHUSWAP LAKE', 'LOWER KOOTENAY', 'GLEN VOWELL',
                         "GWA'SALA-NAKWAXDA'XW", 'GWAWAENUK TRIBE', 'HAGWILGET VILLAGE', 'HAISLA NATION', 'HALALT',
                         'WESTERN COMMAND', 'HALFWAY RIVER FIRST NATION', 'HEILTSUK', 'HESQUIAHT', 'HIGH BAR',
                         'HOMALCO', 'HUPACASATH FIRST NATION', 'HUU-AY-AHT FIRST NATIONS', 'ISKUT',
                         "K'ï¿½ï¿½_MOKS FIRST NATION", 'KOMOKS FIRST NATION',
                         "KA:'YU:'K'T'H'/CHE:K:TLES7ET'H' FIRST NATIONS", 'KANAKA BAR', 'KATZIE', 'KISPIOX', 'KITASOO',
                         'CHEAM', 'CHESLATTA CARRIER NATION', 'COLDWATER', "COOK'S FERRY", 'COWICHAN',
                         "DA'NAXDA'XW FIRST NATION", 'DITIDAHT', 'DOIG RIVER FIRST NATION', 'U OF', 'UNIV',
                         'UNIVERSITIES', 'UNIVERSITY', 'UNIVERSITY COLLEGE', 'DOUGLAS', "DZAWADA'ENUXW FIRST NATION",
                         'EHATTESAHT', "ESK'ETEMC", 'ESQUIMALT', 'FORT NELSON FIRST NATION', 'GITANMAAX', 'GITANYOW',
                         "GITGA'AT FIRST NATION", 'GITSEGUKLA', 'GITWANGAK', 'CANADIAN INSTITUTE FOR THE BLIND',
                         'CATERCORNER', 'CATERPLAN SERVICES', 'CNIB', 'INSTITUTE FOR THE BLIND',
                         'NATIONAL INSTITUTE FOR THE BLIND', 'ROYAL CANADIAN INSTITUTE FOR THE BLIND',
                         'THE BLIND INSTITUTE', 'GITXAALA NATION', "?AKISQ'NUK FIRST NATION", "?ESDILAGH FIRST NATION",
                         "?AQAM", 'ADAMS LAKE', 'AHOUSAHT', 'AITCHELITZ', 'ALEXIS CREEK', 'ASHCROFT', 'BEECHER BAY',
                         'BLUEBERRY RIVER FIRST NATIONS', 'BLINDCRAFT', 'THE BLIND', 'WHITE CANE', 'BONAPARTE',
                         'BOOTHROYD', 'BOSTON BAR FIRST NATION', 'BRIDGE RIVER', 'BURNS LAKE', 'CAMPBELL RIVER',
                         'CANIM LAKE', 'CAPE MUDGE', 'CAYOOSE CREEK', 'REGISTERED RESPIRATORY TECHNOLOGIST',
                         'REGISTERED RESPIRATORY TECHNOLOGIST RRT', 'REGISTERED RESPIRATORY THERAPISTS RRT',
                         'REGISTERED RESPIRATORY THERPISTS', 'RRT', 'REGISTERED MEDICAL OFFICE ASSISTANT', 'RMOA',
                         'SUTTON GROUP', 'ROYAL LEPAGE', 'REALTY WORLD', 'UNIGLOBE', 'REEMARK', 'AGROLOGIST',
                         'AGROLOGISTS', 'PAG', 'PROFESSIONAL AGRICULTURIST', 'ANAVET', 'BRIC', 'CHAMBER OF COMMERCE',
                         'DETECTIVE', 'POLICE', 'POLICING', 'SERGEANT', 'INTRAWEST', 'CHAWATHIL', 'SASKATCHEWAN',
                         'REMAX', 'CENTURY 21', 'CENTURY XXI', 'crossfit', 'cross fit', 'EARTH SCIENCE',
                         'ENVIRONMENTAL GEOLOGY', 'ENVIRONMENTAL GEOSCIENCE', 'EXPLORATION GEOSCIENE', 'GEOCHEMICAL',
                         'GEOCHEMISTRY', 'HYDROGEOLOGICAL', 'VOLCANOLOGY', 'earthscience', 'Fire Fighter',
                         'Fire Fighters', 'Fire Protection', 'Fire Services', 'Firefighter', 'Firefighters',
                         'Fire Department', 'Fire Rescue', 'Fire Suppression', 'CONSULTING ENGINEER', 'ENGINEER',
                         'ENGINEERING', 'INGENIERE', 'INGENIEUR', 'INGENIEUR CONSIEL', 'P ENG', 'PROFESSIONAL ENGINEER',
                         'C1D1', 'LICENSED GRADUATE NURSE', 'NP', 'NURSE', 'NURSES', 'REGISTERED NURSE',
                         'REGISTERED NURSE PRACTITIONER', 'RN', 'LICENSED GRADUATE PSYCHIATRIC NURSE',
                         'REGISTERED PSYCHIATRIC NURSE', 'REGISTERED PSYCHIATRIC NURSES', 'RPN', 'ALFA ROMEO',
                         'CHRYSLER', 'DODGE', 'FIAT', 'JEEP', 'RAM', 'RCPP',
                         'REGISTERED CERTIFIED PROFESSIONAL PURCHASER',
                         'REGISTERED CERTIFIED PROFESSIONAL PURCHASER RCPP', 'DENTAL LAB', 'DENTAL LABORATORY',
                         'DENTAL STUDIO', 'DENTAL TECH', 'DENTAL TECHNICIAN', 'REGISTERED DENTAL TECHNICIAN',
                         'Pest Detective ', 'SQUATITS FIRST NATION', 'SQUAWTITS FIRST NATION', 'SQUWTITS FIRST NATION',
                         'SKWAW-TITS FIRST NATION', 'PETERS FIRST NATION', 'SQUATICH FIRST NATION']

data = [['WM', 'distinctive', 12], ['079', 'distinctive', 3], ['VENTURES', 'descriptive', 1000]]
df = pd.DataFrame(data, columns=['word', 'word_classification', 'frequency'])

df_synonyms = pd.DataFrame(data, columns=['word', 'word_classification', 'frequency'])

data_general = ['an,and,are,as,at,be,but,by,for,if,in,into,is,it,no,not,of,on,or,such,that,the,their,then,there,these,' \
                'they,this,to']
df_general = pd.DataFrame(data_general, columns=['synonyms_text'])

field = 'synonyms_text'
synonym_text_list = ['an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'if', 'in', 'into', 'is', 'it', 'no', \
                     'not', 'of', 'on', 'or', 'such', 'that', 'the', 'their', 'then', 'there', 'these', 'they', 'this',
                     'to']
name = 'MOUNTAIN ASSOCIATION VIEW LIMITED PARTNERSHIP'
#                       [anywhere designation, end designation]
designation_name_list = [['association'], ['limited partnership']]

user_input = 'MOUNTAIN COOPERATIVE VIEW LIMITED LIABILITY PARTNERSHIP'
designation_name_list = ['cooperative', 'limited liability partnership']

entity_type = 'CC'
entity_type_designation_list = [['ccc', 'community contribution company'],
                                ['limited', 'ltd.', 'incorporated', 'inc.', 'corporation', 'corp']]

'''
def test_data_frame_to_list(client, jwt, app):
    assert_that(data_frame_to_list(df), list_dist)
    assert_that(data_frame_to_list(df), list_desc)
    assert_that(data_frame_to_list(df), list_none)


def test_get_list_of_lists(client, jwt, app):
    assert_that(get_list_of_lists(df_general, field), synonym_text_list)


def test_remove_french(client, jwt, app):
    assert_that(remove_french(text, fr_designation_end_list), 'W & M 074 VENTURES INC.')


def test_get_substitution_list(client, jwt, app):
    assert_that(get_substitution_list(substitution_word), ['mount', 'mountain', 'mt', 'mtn'])


def test_is_substitution_word(client, jwt, app):
    assert_that(is_substitution_word(substitution_word), True)


def test_get_stop_word_list(client, jwt, app):
    assert_that(get_stop_word_list(), stop_words)


def test_get_prefix_list(client, jwt, app):
    assert_that(get_prefix_list(), prefix_list)


def test_get_en_designation_any_all_list(client, jwt, app):
    assert_that(get_en_designation_any_all_list(), en_designation_any_list)


def test_get_en_designation_end_all_list(client, jwt, app):
    assert_that(get_en_designation_end_all_list(), en_designation_end_list)


def test_get_fr_designation_end_list(client, jwt, app):
    assert_that(get_fr_designation_end_list(), fr_designation_end_list)


def test_get_designations_in_name(client, jwt, app):
    assert_that(get_designations_in_name(user_input), designation_name_list)
'''

def test_get_designation_by_entity_type(client, jwt, app):
    assert_that(get_designation_by_entity_type(entity_type), entity_type_designation_list)

'''
def test_get_stand_alone_list(client, jwt, app):
    assert_that(get_stand_alone_list(), stand_alone_list)


def test_get_words_to_avoid(client, jwt, app):
    assert_that(get_words_to_avoid(), words_to_avoid)


def test_get_words_requiring_consent(client, jwt, app):
    assert_that(get_words_requiring_consent(), words_require_consent)


def test_get_classification(client, jwt, app):
    assert_that(get_classification(word), 'none')


def test_get_substitution_list(client, jwt, app):
    assert_that(get_substitution_list(substitution_word), ['mount', 'mountain', 'mt', 'mtn'])


def test_is_substitution_word(client, jwt, app):
    assert_that(is_substitution_word(substitution_word), True)


def test_get_stop_word_list(client, jwt, app):
    assert_that(get_stop_word_list(), stop_words)


def test_get_prefix_list(client, jwt, app):
    assert_that(get_prefix_list(), prefix_list)


def test_get_en_designation_any_list(client, jwt, app):
    assert_that(get_en_designation_any_list(), en_designation_any_list)


def test_get_en_designation_end_list(client, jwt, app):
    assert_that(get_en_designation_end_list(), en_designation_end_list)


def test_get_fr_designation_end_list(client, jwt, app):
    assert_that(get_fr_designation_end_list(), fr_designation_end_list)


def test_get_stand_alone_list(client, jwt, app):
    assert_that(get_stand_alone_list(), stand_alone_list)


def test_get_classification(client, jwt, app):
    assert_that(get_classification(word), 'none')


def test_get_substitution_list(client, jwt, app):
    assert_that(get_substitution_list(substitution_word), ['mount', 'mountain', 'mt', 'mtn'])


def test_is_substitution_word(client, jwt, app):
    assert_that(is_substitution_word(substitution_word), True)


def test_get_stop_word_list(client, jwt, app):
    assert_that(get_stop_word_list(), stop_words)


def test_get_prefix_list(client, jwt, app):
    assert_that(get_prefix_list(), prefix_list)


def test_get_en_designation_any_list(client, jwt, app):
    assert_that(get_en_designation_any_list(), en_designation_any_list)


def test_get_en_designation_end_all_list(client, jwt, app):
    assert_that(get_en_designation_end_all_list(), en_designation_end_list)


def test_get_fr_designation_end_list(client, jwt, app):
    assert_that(get_fr_designation_end_list(), fr_designation_end_list)


def test_get_designations_in_name(client, jwt, app):
    assert_that(get_designations_in_name(user_input), designation_name_list)


def test_get_stand_alone_list(client, jwt, app):
    assert_that(get_stand_alone_list(), stand_alone_list)


def test_get_words_to_avoid(client, jwt, app):
    assert_that(get_words_to_avoid(), words_to_avoid)


def test_get_words_requiring_consent(client, jwt, app):
    assert_that(get_words_requiring_consent(), words_require_consent)


def test_get_classification(client, jwt, app):
    assert_that(get_classification(word), 'none')


def test_regex_transform(client, jwt, app):
    assert_that(regex_transform(text, en_designation_any_list, en_designation_end_list, prefix_list), 'WM H VENTURES')


def test_clean_name_words(client, jwt, app):
    assert_that(
        clean_name_words(text, stop_words, en_designation_any_list, en_designation_end_list, fr_designation_end_list, \
                         prefix_list), 'WM 074 VENTURES')
'''