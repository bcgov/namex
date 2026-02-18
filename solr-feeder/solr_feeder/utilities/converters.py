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


def convert_solr_doc(json_string: str) -> dict:
    """Convert a Solr add document to the target format.

    Args:
        json_string: JSON string in Solr add format.

    Returns:
        Converted dictionary in NR or CORP format.
    """
    data = json.loads(json_string)
    doc = data.get('add', {}).get('doc', {})
    source = doc.get('source', '').upper()

    if source == 'NAMEREQUEST':
        return _convert_nr_doc(doc)
    elif source == 'CORP':
        return _convert_corp_doc(doc)
    else:
        raise ValueError(f"Unknown source type: {source}")


def _convert_nr_doc(doc: dict) -> dict:
    """Convert a name request Solr doc to target NR format."""
    # Convert "NR 0664756" -> "NR0664756" (remove space)
    nr_num = doc.get('id', '').replace(' ', '')

    # Convert ISO datetime to date only
    start_date = _extract_date(doc.get('start_date', ''))

    return {
        'nr_num': nr_num,
        'start_date': start_date,
        'jurisdiction': doc.get('jurisdiction', ''),
        'state': doc.get('state_type_cd', ''),
        'type': 'NR',
        'names': [
            {
                'choice': doc.get('choice', -1),
                'name': doc.get('name', ''),
                'name_state': 'A',  # Default to Approved
                'submit_count': 1
            }
        ]
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


def _extract_date(iso_datetime: str) -> str:
    """Extract date portion from ISO datetime string.

    Args:
        iso_datetime: ISO format datetime (e.g., "2026-01-27T14:52:31Z")

    Returns:
        Date string in YYYY-MM-DD format.
    """
    if not iso_datetime:
        return ''
    try:
        dt = datetime.fromisoformat(iso_datetime.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        return iso_datetime[:10] if len(iso_datetime) >= 10 else iso_datetime
