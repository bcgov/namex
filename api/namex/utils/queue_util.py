import uuid
from datetime import datetime, timezone

from flask import current_app
from sbc_common_components.utils.enums import QueueMessageTypes
from simple_cloudevent import SimpleCloudEvent

from namex.services import queue


def publish_email_notification(nr_num: str, option: str, refund_value=None):
    """Send notification info to the mail queue."""
    event_data = {'request': {'nrNum': nr_num, 'option': option}}

    if refund_value:
        event_data['request']['refundValue'] = refund_value

    ce = SimpleCloudEvent(
        id=str(uuid.uuid4()),
        source=f'/requests/{nr_num}',
        subject='namerequest',
        type=QueueMessageTypes.NAMES_MESSAGE_TYPE.value,
        time=datetime.now(tz=timezone.utc).isoformat(),
        data=event_data,
    )

    email_topic = current_app.config.get('EMAILER_TOPIC', 'mailer')
    payload = queue.to_queue_message(ce)
    current_app.logger.debug('About to publish email for %s nrNum=%s', option, nr_num)
    queue.publish(topic=email_topic, payload=payload)


def publish_resend_email_notification(nr_num: str, option: str, resend_event_id: int):
    """Send resend notification info to the mail queue."""
    event_data = {
        'request': {
            'nrNum': nr_num,
            'option': option,
            'resendEventId': resend_event_id  # Include the resend event ID
        }
    }

    ce = SimpleCloudEvent(
        id=str(uuid.uuid4()),
        source=f'/requests/{nr_num}',
        subject='namerequest',
        type=QueueMessageTypes.NAMES_MESSAGE_TYPE.value,
        time=datetime.now(tz=timezone.utc).isoformat(),
        data=event_data,
    )

    email_topic = current_app.config.get('EMAILER_TOPIC', 'mailer')
    payload = queue.to_queue_message(ce)
    current_app.logger.debug('About to publish resend email for %s nrNum=%s, resendEventId=%s', option, nr_num, resend_event_id)
    queue.publish(topic=email_topic, payload=payload)


def create_name_request_state_msg(nr_num, state_cd, old_state_cd):
    """Builds a name request state message."""

    event_data = {'request': {'nrNum': nr_num, 'newState': state_cd, 'previousState': old_state_cd}}

    ce = SimpleCloudEvent(
        id=str(uuid.uuid4()),
        source=f'/requests/{nr_num}',
        subject='namerequest',
        type=QueueMessageTypes.NAMES_EVENT.value,
        time=datetime.now(tz=timezone.utc).isoformat(),
        data=event_data,
    )

    payload = queue.to_queue_message(ce)

    return payload


def send_name_request_state_msg(nr_num, state_cd, old_state_cd):
    """Publish name request state message to pubsub nr state subject."""
    email_topic = current_app.config.get('NAMEX_NR_STATE_TOPIC', 'mailer')
    queue.publish(topic=email_topic, payload=create_name_request_state_msg(nr_num, state_cd, old_state_cd))
    current_app.logger.debug(
        'Published name request ({}) state change from {} -> {}'.format(nr_num, old_state_cd, state_cd)
    )


def create_name_state_msg(nr_num, name_id, state_cd, old_state_cd):
    """Builds a name state message."""

    event_data = {'name': {'nameId': name_id, 'nrNum': nr_num, 'newState': state_cd, 'previousState': old_state_cd}}

    ce = SimpleCloudEvent(
        id=str(uuid.uuid4()),
        source=f'/request/{nr_num}/name/{name_id}',
        subject='namerequest',
        type=QueueMessageTypes.NAMES_EVENT.value,
        time=datetime.now(tz=timezone.utc).isoformat(),
        data=event_data,
    )

    payload = queue.to_queue_message(ce)

    return payload


def send_name_state_msg(nr_num, name_id, state_cd, old_state_cd):
    """Publish name state message to pubsub nr state subject."""
    email_topic = current_app.config.get('NAMEX_NR_STATE_TOPIC', 'mailer')
    queue.publish(topic=email_topic, payload=create_name_state_msg(nr_num, name_id, state_cd, old_state_cd))
