import json
import time
import uuid
from datetime import datetime, timezone

from config import Config
from namex.services import queue
from queue_common.messages import create_cloud_event_msg


def create_name_request_state_msg(nr_num, state_cd, old_state_cd):
    """Builds a name request state message."""
    return create_cloud_event_msg(msg_id=str(uuid.uuid4()),
                                            msg_type='bc.registry.names.events',
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