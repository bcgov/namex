import json
import time
import uuid
from datetime import datetime, timezone

from flask import current_app

from namex.services import queue
from queue_common.messages import create_cloud_event_msg


def publish_email_notification(nr_num: str, option: str, refund_value=None):
    """Send notification info to the mail queue."""
    data = {
        'request': {
            'nrNum': nr_num,
            'option': option
        }
    }

    if refund_value:
        data['request']['refundValue'] = refund_value

    payload = create_cloud_event_msg(
        msg_id=str(uuid.uuid4()),
        msg_type='bc.registry.names.request',
        source=f'/requests/{nr_num}',
        time=datetime.utcfromtimestamp(time.time()).replace(tzinfo=timezone.utc).isoformat(),
        identifier=nr_num,
        json_data_body=data
    )

    email_subject = current_app.config.get('NATS_EMAILER_SUBJECT')
    current_app.logger.debug('About to publish email for %s nrNum=%s', option, nr_num)
    queue.publish_json(payload, email_subject)


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
    # queue.publish_json_to_subject_sync(
    #     create_name_request_state_msg(nr_num, state_cd, old_state_cd),
    #     current_app.config.get('NATS_NR_STATE_SUBJECT')
    # )
    current_app.logger \
        .debug('Published name request ({}) state change from {} -> {}'.format(nr_num, old_state_cd, state_cd))


def create_name_state_msg(nr_num, name_id, state_cd, old_state_cd):
    """Builds a name state message."""
    return create_cloud_event_msg(msg_id=str(uuid.uuid4()),
                                  msg_type='bc.registry.names.events',
                                  source=f'/request/{nr_num}/name/{name_id}',
                                  time=datetime.
                                    utcfromtimestamp(time.time()).
                                    replace(tzinfo=timezone.utc).
                                    isoformat(),
                                  identifier=name_id,
                                  json_data_body={
                                      'name': {
                                          'nameId': name_id,
                                          'nrNum': nr_num,
                                          'newState': state_cd,
                                          'previousState': old_state_cd
                                      }}
                                  )


def send_name_state_msg(nr_num, name_id, state_cd, old_state_cd):
    """Publish name state message to NATS nr state subject."""
    queue.publish_json_to_subject_sync(
        create_name_state_msg(nr_num, name_id, state_cd, old_state_cd),
        current_app.config.get('NATS_NR_STATE_SUBJECT')
    )
