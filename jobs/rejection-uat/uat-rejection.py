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

    sql = "select r.id, r.nr_num, n.choice, n.name, n.decision_text, n.conflict1_num, n.conflict1, n.conflict1_num "\
          "from requests r, names n "\
          "where r.id = n.nr_id and n.state = 'REJECTED' and r.state_cd = 'REJECTED' "\
          "order by  r.submitted_date" \
          "limit " + MAX_ROW_LIMIT

    requests= db.session.execute(sql)
    for request_id, nr_num in requests:
        current_app.logger.debug('processing id: {}'.format(request_id))
        ## TO auto-analyze steps

        #to get the results and format the jsonb column
        #we will nee dto handle the update to the jsonb col and may need to pull stuff out of the reponse issues
        # we will nee dto review each response issue and determine how we will deal with it.


        update_sql = "update events " \
                     "set event_json='{json_input}'::jsonb " \
                     "where id={id}".format(id=event_id, json_input=formatted_json)

        insert_sql = "insert into uat_results " \
                     "(id, nr_num,nr_state, choice, name, name_state, decision_text,  conflict1_num, conflict1, result_state "  \
                     " result_decision_text, result_conflict1_num, result_conflict1, result_response)" \
                     "values"\
                     "( )"

        db.session.execute(insert_sql)
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
