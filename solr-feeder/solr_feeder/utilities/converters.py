# Copyright © 2023 Province of British Columbia
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
"""Converters for transforming Solr document formats."""
import json
from datetime import datetime


# Name-request sources stored on requests.source. NRO is the legacy value.
_NR_SOURCES = {'NAMEREQUEST', 'NRO', 'NAMEX', 'SO'}


def convert_solr_doc(json_string: str) -> dict:
    """Convert a Solr add document to the target format.

    Args:
        json_string: JSON string in Solr add format.

    Returns:
        Converted dictionary in NR or CORP format.
    """
    data = json.loads(json_string)
    if 'delete' in data:
        raise ValueError('Solr delete is not supported; update the document state instead')

    doc = data.get('add', {}).get('doc', {})
    source = (doc.get('source') or '').upper()

    if source == 'CORP':
        return _convert_corp_doc(doc)
    if source in _NR_SOURCES or source == '':
        return _convert_nr_doc(doc)
    raise ValueError(f"Unknown source type: {source}")


def _convert_nr_doc(doc: dict) -> dict:
    """Convert a name request Solr doc to target NR format."""
    # Convert "NR 0664756" -> "NR0664756" (remove space)
    nr_num = doc.get('id', '').replace(' ', '')

    start_date = _solr_datetime(doc.get('start_date', ''))

    names = doc.get('names')
    if not names:
        names = [
            {
                'choice': doc.get('choice', -1),
                'name': doc.get('name', ''),
                'name_state': 'A',  # Default to Approved
                'submit_count': doc.get('submit_count', 1)
            }
        ]

    return {
        'nr_num': nr_num,
        'start_date': start_date,
        'jurisdiction': doc.get('jurisdiction', ''),
        'state': doc.get('state_type_cd', ''),
        'type': 'NR',
        'sub_type': doc.get('sub_type', '-'),
        'names': names
    }


def _convert_corp_doc(doc: dict) -> dict:
    """Convert a corporation Solr doc to target CORP format."""
    # Convert ISO datetime to date only
    # start_date = _extract_date(doc.get('start_date', ''))
    start_date = doc.get('start_date', '')

    return {
        'corp_num': doc.get('id', ''),
        'start_date': start_date,
        'jurisdiction': doc.get('jurisdiction', ''),
        'state': doc.get('state_type_cd', ''),
        'type': 'CORP',
        'name': doc.get('name', '')
    }


def _solr_datetime(iso_datetime: str) -> str:
    """Return a UTC datetime Solr's start_date field accepts.

    Args:
        iso_datetime: ISO format datetime (e.g., "2026-01-27T14:52:31Z")

    Returns:
        Datetime string YYYY-MM-DDTHH:MM:SSZ, or '' when blank.
    """
    if not iso_datetime:
        return ''
    text = iso_datetime[:-1] + '+00:00' if iso_datetime.endswith('Z') else iso_datetime
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        try:
            parsed = datetime.strptime(iso_datetime[:10], '%Y-%m-%d')
        except ValueError:
            return ''
    return parsed.strftime('%Y-%m-%dT%H:%M:%SZ')
