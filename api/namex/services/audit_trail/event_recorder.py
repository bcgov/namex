from flask import current_app
from namex import models
import datetime
import bz2


class EventRecorder(object):

    @staticmethod
    def record(user, action, nr, json):

        event = models.Event(
            eventDate = datetime.utcnow,
            action = action,
            jsonZip = bz2.compress(json),
            nrId = nr.id,
            stateCd = nr.stateCd,
            userId = user.id
        )
        try:
            event.save_to_db()
        except Exception as err:
            current_app.logger.error('AUDIT BROKEN: change was - NRNUM: {}, ACTION: {}, USER {}, JSON{}'
                                     .format(nr.nr_num, action, user.username, json)
                                    )
