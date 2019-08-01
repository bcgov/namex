import sys

from sqlalchemy import text
from datetime import datetime, timedelta

from flask import Flask, g, current_app

from namex import db
from namex.utils.logging import setup_logging

from config import Config
import bz2

setup_logging() ## important to do this first


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app


app = create_app(Config)
start_time = datetime.utcnow()
row_count = 0

try:
    sql = "select id,json_zip " \
          "from events "

    events = db.session.execute(sql)
    for event_id, event_compressed_json in events:
        current_app.logger.debug('processing id: {}'.format(event_id))

        decompressed_json = bz2.decompress(event_compressed_json)

        update_sql = "update event " \
                     "set event_json = \'{decompressed_json}\' " \
                     "where id={id}".format(id=event_id)
        db.session.execute(update_sql)
        db.session.commit()
        row_count += 1

except Exception as err:
    db.session.rollback()
    print('Failed to update events: ', err, err.with_traceback(None), file=sys.stderr)
    exit(1)

app.do_teardown_appcontext()
end_time = datetime.utcnow()
print("job - columns updated: {0} completed in:{1}".format(row_count, end_time-start_time))
exit(0)
