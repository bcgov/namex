from flask import Flask, g, current_app
from config import Config

from namex import db
from namex.services import EventRecorder
from namex.services.nro import NROServices
from namex.services.nro.utils import ora_row_to_dict
from namex.models import Request, Event, State
from corps.utils.logging import setup_logging



setup_logging()

nro = NROServices()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    nro.init_app(app)

    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        ''' Enable Flask to automatically remove database sessions at the
         end of the request or when the application shuts down.
         Ref: http://flask.pocoo.org/docs/patterns/sqlalchemy/
        '''
        if hasattr(g, 'db_nro_session'):
            g.db_nro_session.close()

    return app


def job_result_set(ora_con, max_rows):

    ora_cursor = ora_con.cursor()


    result_set = ora_cursor.execute("""
    SELECT id, name, start_date from namex.solr_dataimport_conflicts_vw@colin_readonly 
    WHERE TRUNC(start_date)  <  to_date('20190510','YYYYMMDD')
    AND ROWNUM <= :max_rows ORDER BY id
    """
                                    , max_rows=max_rows
                                    )

    col_names = [row[0] for row in ora_cursor.description]

    return result_set, col_names


def find_corp_in_namex(id,corp_name):
    sql = "select n.id, n.nr_id, n.name, n.corp_num, n.consumption_date, n.state " \
          "from names n " \
          "where n.corp_num = :id and n.name = :corp_name and n.state in ('APPROVED','CONDITION') "


    name_results = db.session.execute(sql)
    return name_results

def update_consumption_date(name_id):

    sql = "update names" \
          "set consumption_date = :start_date" \
          "where id = : name_id"
    results = db.session.execute(sql)
    return results


def insert_corps_list(id,nr_id, name_id):
    sql = "insert into corps_list" \
          "(corp_num, nr_id, name_id )"\
          "values(:id, nr_id, name_id)"

    results = db.session.execute(sql)
    return results



def job(app, namex_db, nro_connection, user, max_rows=100):

    row_count = 0
    datafix_status = None

    try:
        ora_con = nro_connection
        result, col_names = job_result_set(ora_con, max_rows)

        for r in result:

            row_count += 1
            row = ora_row_to_dict(col_names, r)
            #stuff from the datafix table (from namesp, CPRD)
            corp_num = row['id']
            corp_name = row['name']
            start_date = row['start_date']

            name_results = find_corp_in_namex(id, corp_name)
            for name in name_results:

                if name.consumption_date != start_date:
                    update_consumption_date(name.id)

                insert_corps_list(corp_num, name.nr_id,name.id )

        return row_count

    except Exception as err:
        current_app.logger.error('Update Failed:', err.with_traceback(None))
        return -1
