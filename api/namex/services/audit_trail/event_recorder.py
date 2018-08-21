from flask import current_app
from namex import models
from datetime import datetime
import json
import zlib


class EventRecorder(object):

    @staticmethod
    def record(user, action, nr, data_dict):
        try:
            event = EventRecorder.create_event(user, action, nr, data_dict)
            event.save_to_db()
        except Exception as err:
            current_app.logger.error('AUDIT BROKEN: change was - NRNUM: {}, ACTION: {}, USER {}, JSON{}'
                                     .format(nr.nr_num, action, user.username, data_dict)
                                    )

    @staticmethod
    def create_event(user, action, nr, data_dict):

        event = models.Event(
            eventDate = datetime.utcnow(),
            action = action,
            jsonZip = zlib.compress(json.dumps(data_dict).encode('utf8')),
            nrId = nr.id,
            stateCd = nr.stateCd,
            userId = user.id
        )
        return event

