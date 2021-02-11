# Copyright © 2019 Province of British Columbia
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
"""The Test Suites to ensure that the worker is operating correctly."""
import json


def test_extract_payment_token():
    """Assert that the payment token can be extracted from the Queue delivered Msg."""
    from namex_pay.worker import extract_message
    from stan.aio.client import Msg
    import stan.pb.protocol_pb2 as protocol

    # setup
    token = {'paymentToken': {'id': 1234, 'statusCode': 'COMPLETED'}}
    msg = Msg()
    msg.proto = protocol.MsgProto
    msg.proto.data = json.dumps(token).encode('utf-8')

    # test and verify
    assert extract_message(msg) == token
