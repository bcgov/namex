# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""All of the message templates used across the various services."""
import json

import nats


def create_payment_msg(identifier, status):
    """Create a payment payload for the paymentToken."""
    payment_msg = {'paymentToken': {'id': identifier, 'statusCode': status}}
    return payment_msg


def get_payment_id_from_msg(msg: nats.aio.client.Msg):
    """Extract the payment if from the NATS message."""
    try:
        token = json.loads(msg.data.decode('utf-8'))
        return token['paymentToken'].get('id')
    except (AttributeError, NameError, json.decoder.JSONDecodeError):
        return None


def create_cloud_event_msg(msg_id, msg_type, source, time, identifier, json_data_body):  # pylint: disable=too-many-arguments # noqa E501
    # industry standard arguments for this message
    """Create a payload for the email service."""
    cloud_event_msg = {
        'specversion': '1.x-wip',
        'type': msg_type,
        'source': source,
        'id': msg_id,
        'time': time,
        'datacontenttype': 'application/json',
        'identifier': identifier
    }
    if json_data_body:
        cloud_event_msg['data'] = json_data_body

    return cloud_event_msg
