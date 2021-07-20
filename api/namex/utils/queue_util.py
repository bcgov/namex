import json
import time
import uuid
from datetime import datetime, timezone

from config import Config
from namex.services import queue


def create_cloud_event_msg(msg_id, msg_type, source, time, identifier, json_data_body):  # pylint: disable=too-many-arguments # noqa E501
    # industry standard arguments for this message
    """Creates a payload for the cloud event messages."""
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

def create_name_request_state_msg(nr_num, state_cd, old_state_cd):
    """Builds a name request state message."""
    return create_cloud_event_msg(msg_id=str(uuid.uuid4()),
                                            msg_type='bc.registry.names.request',
                                            source=f'/requests/{nr_num}',
                                            time=datetime.
                                            utcfromtimestamp(time.time()).
                                            replace(tzinfo=timezone.utc).
                                            isoformat(),
                                            identifier=nr_num,
                                            json_data_body={
                                                'request': {
                                                    'nrNum': nr_num,
                                                    'newState': state_cd,
                                                    'previousState': old_state_cd
                                                }}
                                            )

def send_name_request_state_msg(nr_num, state_cd, old_state_cd):
    """Publish name request state message to NATS nr state subject."""
    queue.publish_json_to_subject_sync(
        create_name_request_state_msg(nr_num, state_cd, old_state_cd), 
        Config.NATS_NR_STATE_SUBJECT
    )