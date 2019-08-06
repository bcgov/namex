import sys, os
from datetime import datetime, timedelta
from flask import Flask, g, current_app
from namex import db
from namex.utils.logging import setup_logging

from config import Config
import zlib, json


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
MAX_ROW_LIMIT = os.getenv('MAX_ROWS', '100')

try:

    sql = "select id,substring(json_zip,3) " \
          "from events where event_json is null limit " + MAX_ROW_LIMIT

    events = db.session.execute(sql)
    for event_id, event_compressed_json in events:
        current_app.logger.debug('processing id: {}'.format(event_id))
        x = bytearray.fromhex(event_compressed_json)
        z = zlib.decompress(x)
        json_str =  z.decode('utf8')
        escaped_json_str = json_str.replace("'", "''")
        new_text = escaped_json_str.replace(":Final ",". Final ")
        new_text1 = new_text.replace("Fax #:","Fax ")

        json_list = json.loads(new_text1)

        formatted_json = json.dumps(json_list)

        update_sql = "update events " \
                     "set event_json='{json_input}'::jsonb "  \
                     "where id={id}".format(id=event_id, json_input=formatted_json)

        print(update_sql)
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
