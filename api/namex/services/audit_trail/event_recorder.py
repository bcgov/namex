import json
from datetime import datetime

from flask import current_app

from namex.models import Event, User


class EventRecorder(object):

    @staticmethod
    def record(user, action, nr, data_dict, save_to_session=False):
        """Record an event."""
        try:
            event = EventRecorder.create_event(user, action, nr, data_dict)
            if save_to_session:
                event.save_to_session()
            else:
                event.save_to_db()
        except Exception as err:
            current_app.logger.error(err.with_traceback(None))
            current_app.logger.error('AUDIT BROKEN: change was - NRNUM: {}, ACTION: {}, USER {}, JSON{}'
                                     .format(nr.nrNum, action, user.username, data_dict))

    @staticmethod
    def record_as_system(action, nr, data_dict, save_to_session=False):
        """Record an event as a system user."""
        try:
            user = User.get_service_account_user()
            if user:
                event = EventRecorder.create_event(user, action, nr, data_dict)
                if save_to_session:
                    event.save_to_session()
                else:
                    event.save_to_db()
        except Exception as err:
            current_app.logger.error(err.with_traceback(None))
            current_app.logger.error('AUDIT BROKEN: change was - NRNUM: {}, ACTION: {}, USER {}, JSON{}'
                                     .format(nr.nrNum, action, user.username, data_dict))

    @staticmethod
    def create_event(user, action, nr, data_dict):
        """Create an event object."""
        event = Event(
            eventDate=datetime.utcnow(),
            action=action,
            eventJson=json.dumps(data_dict),
            nrId=nr.id,
            stateCd=nr.stateCd,
            userId=user.id if user else None
        )
        return event
