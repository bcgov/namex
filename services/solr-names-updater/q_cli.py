#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
"""Service for listening and handling Queue Messages.

This service registers interest in listening to a Queue and processing received messages.
"""
import asyncio
import functools
import getopt
import json
import os
import random
import signal
import sys
import uuid

from nats.aio.client import Client as NATS  # noqa N814; by convention the name is NATS
from stan.aio.client import Client as STAN  # noqa N814; by convention the name is STAN

from queue_common.service_utils import error_cb, logger, signal_handler


async def run(loop, payload_values):  # pylint: disable=too-many-locals
    """Run the main application loop for the service.

    This runs the main top level service functions for working with the Queue.
    """
    # NATS client connections
    nc = NATS()
    sc = STAN()

    async def close():
        """Close the stream and nats connections."""
        await sc.close()
        await nc.close()

    # Connection and Queue configuration.
    def nats_connection_options():
        return {
            'servers': os.getenv('NATS_SERVERS', 'nats://127.0.0.1:4222').split(','),
            'io_loop': loop,
            'error_cb': error_cb,
            'name': os.getenv('NATS_CLIENT_NAME', 'namex.solr.names.updater.tester')
        }

    def stan_connection_options():
        return {
            'cluster_id': os.getenv('NATS_CLUSTER_ID', 'test-cluster'),
            'client_id': str(random.SystemRandom().getrandbits(0x58)),
            'nats': nc
        }

    def subscription_options():
        return {
            'subject': os.getenv('NATS_SUBJECT', 'namerequest.state'),
            'queue': os.getenv('NATS_QUEUE', 'namerequest-processor'),
            'durable_name': os.getenv('NATS_QUEUE', 'namerequest-processor') + '_durable'
        }

    try:
        # Connect to the NATS server, and then use that for the streaming connection.
        await nc.connect(**nats_connection_options())
        await sc.connect(**stan_connection_options())

        # register the signal handler
        for sig in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(getattr(signal, sig),
                                    functools.partial(signal_handler, sig_loop=loop, sig_nc=nc, task=close)
                                    )

        msg_id = str(uuid.uuid4())
        nr_num = payload_values.get('nr_num')
        source = f'/requests/{nr_num}'

        payload = {
            'specversion': '1.0.1',
            'type': 'bc.registry.names.events',
            'source': source,
            'id': msg_id,
            'time': '',
            'datacontenttype': 'application/json',
            'identifier': nr_num,
            'data': {
                'request': {
                    'nrNum': nr_num,
                    'newState': payload_values.get('new_state'),
                    'previousState': payload_values.get('prev_state')
                }
            }
        }
        await sc.publish(subject=subscription_options().get('subject'),
                         payload=json.dumps(payload).encode('utf-8'))

    except Exception as e:  # pylint: disable=broad-except
        # TODO tighten this error and decide when to bail on the infinite reconnect
        logger.error(e)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:n:p:', ['nrnum=', 'newstate=', 'prevstate='])
    except getopt.GetoptError:
        print('q_cli.py -nr <nr_num> -ns <new_state> -ps <previous_state>')
        print('e.g. q_cli.py -i "NR 5659951" -n APPROVED -p DRAFT')
        sys.exit(2)
    nr_num, new_state, prev_state = None, None, None
    for opt, arg in opts:
        if opt in ('-i', '--nrnum'):
            nr_num = arg
        elif opt in ('-n', '--newstate'):
            new_state = arg
        elif opt in ('-p', '--prevstate'):
            prev_state = arg
    if not nr_num or not new_state or not prev_state:
        print('q_cli.py -nr <nr_num> -ns <new_state> -ps <previous_state>')
        print('e.g. q_cli.py -i "NR 5659951" -n APPROVED -p DRAFT')
        sys.exit()

    payload_values = {
        'nr_num': nr_num,
        'new_state': new_state,
        'prev_state': prev_state
    }
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run(event_loop, payload_values))
