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


def job_result_set(ora_con, max_rows):

    ora_cursor = ora_con.cursor()


    result_set = ora_cursor.execute("""
    SELECT id, name, start_date from namex.solr_dataimport_conflicts_vw@colin_readonly 
    WHERE TRUNC(start_date)  <  to_date('20190510','YYYYMMDD') and id > 'S0033034'
     ORDER BY id
    """

                                    )



    col_names = [row[0] for row in ora_cursor.description]

    return result_set, col_names

def find_corp_count_in_namex(id, corp_name):
    sql = "select count(*) as name_count " \
          "from names n " \
          "where n.corp_num = '{id}' and n.name = '{corp_name}' and n.state in ('APPROVED','CONDITION') ".format(id=id, corp_name=corp_name)

    print(sql)
    name_results =  db.session.execute(sql)
    for n in name_results:
        name_count  = n['name_count']



    return name_count


def find_corp_in_namex(id,corp_name):
    sql = "select n.id, n.nr_id, n.name, n.corp_num, n.consumption_date, n.state " \
          "from names n " \
          "where n.corp_num = '{id}' and n.name = '{corp_name}' and n.state in ('APPROVED','CONDITION') ".format(id=id, corp_name=corp_name)

    print(sql)
    name_results = db.session.execute(sql)
    return name_results

def update_consumption_date(name_id,start_date):

    #need to deal with utc consumption_date check extractor

    update_sql = "update names " \
          "set consumption_date =  '{start_date}' " \
          "where id =  {name_id}".format(name_id=name_id, start_date=start_date)

    print(update_sql)
    results = db.session.execute(update_sql)
    return results


def insert_missing_corps_list(corp_num,corp_name):
    insert_sql = "insert into missing_corps" \
          "(corp_num, corp_name )"\
          "values('{corp_num}', '{corp_name}')".format(corp_num=corp_num, corp_name=corp_name)

    print(insert_sql)

    results = db.session.execute(insert_sql)
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
        ora_con = nro_connection
        result, col_names = job_result_set(ora_con, max_rows)

        for r in result:

            row_count += 1
            if row_count > max_rows:
                return row_count

            row = ora_row_to_dict(col_names, r)

            corp_num = row['id']
            corp_name =row['name']


            corp_name=corp_name.replace('\'', "''")
            start_date = row['start_date']

            name_count = find_corp_count_in_namex(corp_num, corp_name)
            if name_count == 0:
                #these are the ones that need to be datafixed in namesp to geta valid consumed NR into Namex
                insert_missing_corps_list(corp_num,corp_name)
            else:

                name_results = find_corp_in_namex(corp_num, corp_name)
                for name in name_results:
                    if name.consumption_date:
                        test_date = name.consumption_date
                        test_date = test_date.date()
                    else:
                        test_date = None

                    test_start_date = start_date.date()

                    if test_date != test_start_date:
                        update_consumption_date(name.id,start_date)

                    #these are the active corps in namex and will be used to find the cnsumed names that shoudl be set to historical
                    #any names that dont match to this list shoudl be set to historical at the request level.
                    insert_active_corps_list(corp_num, corp_name, name.nr_id,name.id )

            db.session.commit()
        return row_count

    except Exception as err:
        current_app.logger.error('Update Failed:', err.with_traceback(None))
        return -1
