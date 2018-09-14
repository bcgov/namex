
import datetime
import fnmatch
import json
import os
from os import path
import pathlib
import zipfile

import untangle


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


def log(line, file, message):
    output = '{} {} : {}'.format(line, file, message)
    print(output)
    logfile.write(output + '\n')

    if count % 100 == 0:
        logfile.flush()


def dump_json(data_dict):
    json.dump(data_dict, jsonfile)
    jsonfile.write('\n')

    if count % 100 == 0:
        jsonfile.flush()


def strip_values(data_dict: dict):
    for key in data_dict.keys():
        data_dict[key] = data_dict[key].strip()


# The first thing we do is unzip the zip files. Since this only needs to be done once and takes a long time, an
# indicator file with the extension .done_unzip is used so that we can skip these steps on subsequent runs.
SKIP_UNZIP = True  # It's time consuming just to iterate through all the xml files. Maybe find .zips instead of walk.
if not SKIP_UNZIP:
    for root, dirs, files in os.walk(SOURCE_DIRECTORY):
        for filename in fnmatch.filter(files, '*.zip'):
            fq_filename = os.path.join(root, filename)

            done_file = fq_filename + '.done_unzip'
            if path.isfile(done_file):
                print('{}: already done'.format(fq_filename))
            else:
                print('{}: unzipping'.format(fq_filename))
                destination_directory = os.path.join(root, os.path.splitext(filename)[0])
                zipfile.ZipFile(fq_filename).extractall(destination_directory)
                pathlib.Path(done_file).touch()
                print('{}: unzipped'.format(fq_filename))


# Dev tool - skip ahead to this file (not the filename, but the count of files in the log). For normal use should be 0.
JUMP = 0

# Now do the extract of data and XML generation if the data is mostly complete.
count = 0
for root, dirs, files in os.walk(SOURCE_DIRECTORY):
    matches = fnmatch.filter(files, '*.xml')
    #  matches.sort()  # This needs to sort numerically.

    for filename in matches:
        count = count + 1

        if count < JUMP:
            continue

        fq_filename = os.path.join(root, filename)

        # Convert the file into a python object.
        document = untangle.parse(fq_filename)

        # Load the root object of all the fields we want. This will definitely fail if we load files like the schema
        # fields near the end of the archive. Log as an error and keep processing.
        try:
            trademark = document.tmk_TrademarkApplication.tmk_TrademarkBag.tmk_Trademark
        except AttributeError:
            log(count, fq_filename, 'ERROR: no data (schema file?)')

            continue

        # Check the category first, as it is a common reason to ignore the file.
        featureCategory = trademark.tmk_MarkRepresentation.tmk_MarkFeatureCategory.cdata
        if featureCategory != 'Word':
            log(count, fq_filename, 'skipped: Feature Category is {}'.format(featureCategory))

            continue

        data = dict()

        # Check the status second, as it is a common reason to ignore the file.
        data['status'] = trademark.tmk_MarkCurrentStatusCode.cdata
        if data['status'] in INACTIVE_STATUSES:
            log(count, fq_filename, 'skipped: {}'.format(data['status']))

            continue

        data['application_number'] = trademark.com_ApplicationNumber.com_ST13ApplicationNumber.cdata
        data['category'] = trademark.tmk_MarkCategory.cdata
        data['name'] = trademark.tmk_MarkRepresentation.tmk_MarkReproduction.tmk_WordMarkSpecification. \
            tmk_MarkSignificantVerbalElementText.cdata

        # The description may be missing. These need to be investigated but we'll include them for now.
        try:
            description = trademark.tmk_GoodsServicesBag.tmk_GoodsServices.tmk_ClassDescriptionBag.tmk_ClassDescription
            if type(description) is list:
                text = ''
                for element in description:
                    text = text + ' ' + element.tmk_GoodsServicesDescriptionText.cdata

                data['description'] = text
            else:
                data['description'] = description.tmk_GoodsServicesDescriptionText.cdata
        except AttributeError:
            pass

        # Get rid of leading and trailing spaces.
        strip_values(data)

        if len(data) == 5:
            # We have complete data - write it to the file.
            dump_json(data)
            log(count, fq_filename, 'written to JSON file')
        elif len(data) == 4 and 'description' not in data:
            # We have most of the data we need - write it to the file. These will need to be analyzed to see what could
            # be done differently.
            dump_json(data)
            log(count, fq_filename, 'written to JSON file; missing DESCRIPTION')
        else:
            # Print a nice error message explaining what fields are missing. These will need to be analyzed to see what
            # could be done differently.
            missing = list({'application_number', 'name', 'description', 'status', 'category'} - set(data.keys()))
            missing.sort()

            log(count, fq_filename, 'ERROR missing data: {}'.format(', '.join(missing)))
