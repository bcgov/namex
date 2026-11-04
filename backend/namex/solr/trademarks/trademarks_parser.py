
import datetime
import json
import os
import zipfile

import xmltodict


# This is the directory under which the XML files reside. If they are in ZIP files, they will be unzipped first.
SOURCE_DIRECTORY = 'C:\\TEMP\\Trademarks'


# We do not want to include trademarks that are inactive. The possible status values from the schema are:
#
#   - Action before court of justice pending
#   - Appeal pending
#   - Application accepted
#   - Application Filed
#   - Application published
#   - Application refused
#   - Application withdrawn
#   - Classification checked
#   - Conversion requested
#   - Filing date accorded
#   - Interruption of proceeding
#   - Invalidity proceeding pending
#   - Opposition pending
#   - Registration cancelled
#   - Registration published
#   - Registration surrendered
#   - Revocation proceeding pending
#
INACTIVE_STATUSES = [
    'Application refused', 'Application withdrawn', 'Registration cancelled', 'Registration surrendered']


# This is hokey but faster than figuring out the logging. Log our actions so that we can look back if we ever need to.
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
logfile = open('trademarks-' + timestamp + '.log', 'w')
jsonfile = open('trademarks-' + timestamp + '.json', 'w')


def log(file, message):
    output = '{} : {}'.format(file, message)
    print(output)
    logfile.write(output + '\n')
    logfile.flush()


def dump_json(data_dict):
    json.dump(data_dict, jsonfile)
    jsonfile.write('\n')
    jsonfile.flush()


def strip_values(data_dict: dict):
    for key in data_dict.keys():
        data_dict[key] = data_dict[key].strip()


def process_zip(xml_filename, xml_text):
    data = xmltodict.parse(xml_text)

    # Load the root object of all the fields we want. This will definitely fail if we load files like the schema
    # fields near the end of the archive. Log as an error and keep processing.
    try:
        trademark = data['tmk:TrademarkApplication']['tmk:TrademarkBag']['tmk:Trademark']
    except AttributeError:
        log(xml_filename, 'ERROR: no data (schema file?)')

        return

    # Check the category first, as it is a common reason to ignore the file.
    feature_category = trademark['tmk:MarkRepresentation']['tmk:MarkFeatureCategory']
    if feature_category != 'Word':
        log(xml_filename, 'skipped: Feature Category is {}'.format(feature_category))

        return

    data = dict()

    # Check the status second, as it is a common reason to ignore the file.
    data['status'] = trademark['tmk:MarkCurrentStatusCode']
    if data['status'] in INACTIVE_STATUSES:
        log(xml_filename, 'skipped: {}'.format(data['status']))

        return

    data['application_number'] = trademark['com:ApplicationNumber']['com:ST13ApplicationNumber']
    data['category'] = trademark['tmk:MarkCategory']
    data['name'] = trademark['tmk:MarkRepresentation']['tmk:MarkReproduction']['tmk:WordMarkSpecification']\
        ['tmk:MarkSignificantVerbalElementText']

    try:
        data['registration_number'] = trademark['com:RegistrationNumber']
    except KeyError:
        pass

    # The description may be missing. These need to be investigated but we'll include them for now.
    try:
        description = trademark['tmk:GoodsServicesBag']['tmk:GoodsServices']['tmk:ClassDescriptionBag']\
            ['tmk:ClassDescription']
        if type(description) is list:
            text = ''
            for element in description:
                text = text + ' ' + element['tmk:GoodsServicesDescriptionText']['#text']
        else:
            text = description['tmk:GoodsServicesDescriptionText']['#text']

        data['description'] = text
    except KeyError:
        pass

    # Get rid of leading and trailing spaces.
    strip_values(data)

    if len(data) == 6:
        # We have complete data - write it to the file.
        dump_json(data)
        log(xml_filename, 'written to JSON file')
    elif len(data) == 5 and 'description' not in data:
        # We have most of the data we need - write it to the file. These will need to be analyzed to see what could
        # be done differently.
        dump_json(data)
        log(xml_filename, 'written to JSON file; missing DESCRIPTION')
    elif len(data) == 5 and 'registration_number' not in data:
        # We have most of the data we need - write it to the file. These will need to be analyzed to see what could
        # be done differently.
        dump_json(data)
        log(xml_filename, 'written to JSON file; missing REGISTRATION_NUMBER')
    elif len(data) == 4 and 'description' not in data and 'registration_number' not in data:
        # We have most of the data we need - write it to the file. These will need to be analyzed to see what could
        # be done differently.
        dump_json(data)
        log(xml_filename, 'written to JSON file; missing DESCRIPTION and REGISTRATION_NUMBER')
    else:
        # Print a nice error message explaining what fields are missing. These will need to be analyzed to see what
        # could be done differently.
        missing = list({'application_number', 'registration_number', 'name', 'description', 'status', 'category'} -
                       set(data.keys()))
        missing.sort()

        log(xml_filename, 'ERROR missing data: {}'.format(', '.join(missing)))


# Make it a little quicker to jump to a particular file for debugging.
JUMP = None  # '662169-00.xml'


def load_zip(zip_filename):
    with zipfile.ZipFile(zip_filename) as zip_file:
        for xml_filename in zip_file.namelist():
            if JUMP and xml_filename != JUMP:
                continue

            if xml_filename.endswith('.xml'):
                with zip_file.open(xml_filename) as file:
                    process_zip(fq_filename + ':' + xml_filename, file.read().decode())


# Now do the extract of data and XML generation if the data is mostly complete.
for root, dirs, files in os.walk(SOURCE_DIRECTORY):
    for filename in files:
        if not filename.endswith('Schemas.zip'):
            fq_filename = os.path.join(root, filename)
            if zipfile.is_zipfile(fq_filename):
                load_zip(fq_filename)
