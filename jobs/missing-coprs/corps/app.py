from flask import Flask, g, current_app
from config import Config

from namex import db
from namex.services.nro import NROServices
from namex.services.nro.utils import ora_row_to_dict
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

def get_active_corp_info(ora_con,corp_num):
    ora_cursor = ora_con.cursor()
    result_set = ora_cursor.execute("""
    SELECT id, name, start_date from namex.solr_dataimport_conflicts_vw@colin_readonly 
    WHERE id = :corp_num
    """,

                     corp_num = corp_num )
    col_names = [row[0] for row in ora_cursor.description]

    return result_set, col_names

def pg_job_results(max_rows):
    sql = "select * " \
          "from missing_corps " \
          "where skip='N' "

    print(sql)
    results = db.session.execute(sql)
    return results

def find_corp_name_count_in_namex(id, corp_name):
    sql = "select count(*) as name_count " \
          "from names n " \
          "where n.name = '{corp_name}' and n.state in ('APPROVED','CONDITION') and n.corp_num is null".format(corp_name=corp_name)

    print(sql)
    name_results =  db.session.execute(sql)
    for n in name_results:
        name_count  = n['name_count']

    return name_count


def find_corp_name_in_namex(id,corp_name):
    sql = "select n.id, n.nr_id, n.name, n.corp_num, n.consumption_date, n.state " \
          "from names n " \
          "where n.name = '{corp_name}' and n.state in ('APPROVED','CONDITION') and n.corp_num is null".format(corp_name=corp_name)

    print(sql)
    name_results = db.session.execute(sql)
    return name_results

def update_consumption_info(name_id,corp_num,start_date):

    update_sql = "update names " \
          "set consumption_date =  '{start_date}' " \
          " corp_num = '{corp_num}'" \
          "where id =  {name_id}".format(name_id=name_id, corp_num=corp_num,start_date=start_date)

    print(update_sql)
    results = db.session.execute(update_sql)
    return results


def update_missing_corps_list(corp_num):
    update_sql = "update missing_corps" \
          "set skip='D'"\
          "where corp_num = '{corp_num}')".format(corp_num=corp_num)

    print(update_sql)

    results = db.session.execute(update_sql)
    return results


def insert_active_corps_list(corp_num, corp_name, nr_id, name_id):
    insert_sql = "insert into active_corps" \
          "(corp_num, corp_name, nr_id, name_id )"\
          "values('{corp_num}', '{corp_name}', {nr_id}, {name_id})".format(corp_num=corp_num, corp_name=corp_name, nr_id=nr_id, name_id=name_id)

    print(insert_sql)

    results = db.session.execute(insert_sql)
    return results

def job(app, db, nro_connection, max_rows=100):

    row_count = 0

    try:

        results = pg_job_results(max_rows)
        ora_con = nro_connection

        for r in results:

            row_count += 1
            if row_count > max_rows:
                return row_count

            row = ora_row_to_dict(col_names, r)

            corp_num = r.corp_num
            corp_name =r.corp_name

            corp_name=corp_name.replace('\'', "''")

            active_corp, col_names = get_active_corp_info(ora_con,corp_num)
            row = ora_row_to_dict(col_names, r)
            start_date = row['start_date']


            name_count = find_corp_name_count_in_namex(corp_name)
            if name_count == 0:
                #update skip='D'
                update_missing_corps_list(corp_num)
            else:

                name_results = find_corp_name_in_namex(corp_name)
                for name in name_results:
                    update_consumption_info(name.id,corp_num,start_date)
                    insert_active_corps_list(corp_num, corp_name, name.nr_id,name.id )

            db.session.commit()
        return row_count

    except Exception as err:
        current_app.logger.error('Update Failed:', err.with_traceback(None))
        return -1
