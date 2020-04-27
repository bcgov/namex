import sys, os
from datetime import datetime, timedelta
from flask import Flask, g, current_app
from sqlalchemy import text
from namex import db
from namex.utils.logging import setup_logging
from namex.services.name_request.auto_analyse.protected_name_analysis import ProtectedNameAnalysisService

from config import Config

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
MAX_ROW_LIMIT = os.getenv('MAX_ROWS', '10000')


try:

    sql = "select id,name " \
          "from names where clean_name is null and state='APPROVED'" \
          " limit " + MAX_ROW_LIMIT

    names = db.session.execute(sql)
    for id, name in names:
        current_app.logger.debug('processing id: {}'.format(id))
        #add name processing like in names
        service = ProtectedNameAnalysisService()
        np_svc = service.name_processing_service
        np_svc.set_name(name)
        cleaned_name = np_svc.processed_name
        cleaned_name = cleaned_name.upper()

        update_sql = "update names " \
                     "set clean_name='{cleaned_name}' " \
                     "where id={id}".format(id=id, cleaned_name=cleaned_name)

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
