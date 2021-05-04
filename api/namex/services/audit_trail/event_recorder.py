from flask import current_app
from namex.models import Event
from datetime import datetime
import json



class EventRecorder(object):

    @staticmethod
    def record(user, action, nr, data_dict, save_to_session=False):
        try:
            event = EventRecorder.create_event(user, action, nr, data_dict)
            if save_to_session:
                event.save_to_session()
            else:
                event.save_to_db()
        except Exception as err:
            current_app.logger.error('AUDIT BROKEN: change was - NRNUM: {}, ACTION: {}, USER {}, JSON{}'
                                     .format(nr.nr_num, action, user.username, data_dict)
                                    )

    @staticmethod
    def create_event(user, action, nr, data_dict):
        event = Event(
            eventDate = datetime.utcnow(),
            action = action,
            eventJson = json.dumps(data_dict),
            nrId = nr.id,
            stateCd = nr.stateCd,
            userId = user.id
        )
        return event

