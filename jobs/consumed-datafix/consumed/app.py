from flask import Flask, g, current_app
from config import Config

from namex import db
from namex.services import EventRecorder
from namex.services.nro import NROServices
from namex.services.nro.utils import ora_row_to_dict
from namex.models import Request, Event, State
from consumed.utils.logging import setup_logging



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
    SELECT * 
    FROM (SELECT  df.ID, df.NR_NUM, df.corp_num, df.STATUS, corp.name
    FROM namex_datafix df
    INNER JOIN namex.solr_dataimport_conflicts_vw@colin_readonly corp on corp.id = df.corp_num
    WHERE(df.fd = 'FD' and df.status is null) or (df.status='ERROR') order  by  df.id)
    WHERE ROWNUM <= :max_rows
    """
                                    , max_rows=max_rows
                                    )

    col_names = [row[0] for row in ora_cursor.description]

    return result_set, col_names

def get_name_count(ora_con1, corp_num, corp_name):
    ora_cursor = ora_con1.cursor()
    result_set = ora_cursor.execute("""
                   SELECT
                   COUNT(*) as occurence
                   FROM  name_instance ni
                   LEFT OUTER JOIN name n ON  n.name_id = ni.name_id
                   LEFT OUTER JOIN request r ON r.request_id = n.request_id
                   LEFT OUTER JOIN name_state ns ON  ns.name_id = ni.name_id
                   WHERE ni.corp_num = :corp_num AND ni.end_event_id IS  NULL and ni.name = :corp_name
                   AND ns.end_event_id IS NULL and ns.name_state_type_cd in ('A', 'C')
                   """
                                    , corp_num=corp_num
                                    , corp_name=corp_name
                                    )
    col_ni = [row[0] for row in ora_cursor.description]

    return result_set, col_ni

def get_name_instance_rows(ora_con2, corp_num, corp_name):
    ora_cursor = ora_con2.cursor()
    result_set = ora_cursor.execute("""
               SELECT
               r.nr_num, ni.corp_num, ni.consumption_date
               FROM  name_instance ni
               LEFT OUTER JOIN name n ON  n.name_id = ni.name_id
               LEFT OUTER JOIN request r ON r.request_id = n.request_id
               LEFT OUTER JOIN name_state ns ON  ns.name_id = ni.name_id
               WHERE ni.corp_num = :corp_num AND ni.end_event_id IS  NULL and ni.name = :corp_name
               AND ns.end_event_id IS NULL and ns.name_state_type_cd in ('A', 'C')
               """
                                    , corp_num=corp_num
                                    , corp_name=corp_name
                         )
    col_ni = [row[0] for row in ora_cursor.description]

    return result_set, col_ni




def update_datafix_row(ora_con, id, nr_num, status):

    try:
        ora_cursor = ora_con.cursor()

        result_set = ora_cursor.execute("""
            update NAMEX.NAMEX_DATAFIX 
			set STATUS = :status,
			    NR_NUM = :nr_num
            where id = :id
            """
            ,id=id
            ,nr_num=nr_num
            ,status=status
        )

        print('rows updated',ora_cursor.rowcount)
        if ora_cursor.rowcount > 0:
            return True
    except Exception as err:
        current_app.logger.error('UNABLE TO UPDATE NAMEX_DATAFIX :', err.with_traceback(None))

    return False


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
            nr_num = row['nr_num']
            corp_num = row['corp_num']
            corp_name = row['name']

           #check to see if there are any
            ora_con1 = nro_connection
            name_count_results, col_ni_count = get_name_count(ora_con1, corp_num, corp_name)
            ni_count_row = ora_row_to_dict(col_ni_count, name_count_results)

            #no mathcing name instnace rows
            test = ni_count_row['occurence']
            if test[0] == 0:

                #current_app.logger.error(err.with_traceback(None))
                success = update_datafix_row(ora_con
                                             , id=row['id']
                                             , nr_num=nr_num
                                             , status='BAD'
                                             )
            else:

                #check for name_instance corp rows
                ora_con2 = nro_connection
                name_results, col_ni = get_name_instance_rows(ora_con2, corp_num, corp_name)



                for ni in name_results:
                    ni_row = ora_row_to_dict(col_ni, ni)
                    if ni_row['nr_num'] !=  nr_num:
                        nr_num = ni_row['nr_num']

                    nr = Request.find_by_nr(nr_num)
                    if nr.stateCd == 'HISTORICAL':
                        continue

                    current_app.logger.debug('processing: {}, NameX state: {}'
                                .format(
                                nr_num,
                                None if (not nr) else nr.stateCd[0:9]
                                ))
                    try:
                        nr = nro.fetch_nro_request_and_copy_to_namex_request(user, nr_number=nr_num, name_request=nr)

                        nr._source='NRO'
                        nr.furnished = 'Y'
                        #for ones that are mistakenely set as HISTORICAL, set to APPROVED as this is an active corp

                        namex_db.session.add(nr)
                        EventRecorder.record(user, Event.UPDATE_FROM_NRO, nr, {}, save_to_session=True)
                        current_app.logger.debug('EventRecorder should have been saved to by now, although not committed')

                        datafix_status = None if (not nr) else nr.stateCd

                        success = update_datafix_row(ora_con
                                            , id=row['id']
                                            , nr_num=nr_num
                                            , status=datafix_status
                                            )

                        if success:
                            ora_con.commit()
                            current_app.logger.debug('Oracle commit done')
                            namex_db.session.commit()
                            current_app.logger.debug('Postgresql commit done')
                        else:
                            raise Exception()

                    except Exception as err:
                        current_app.logger.error(err.with_traceback(None))
                        success = update_datafix_row(ora_con
                                            , id=row['id']
                                            , nr_num = nr_num
                                            , status='ERROR'
                                    )
                        namex_db.session.rollback()
                        ora_con.commit()


        return row_count

    except Exception as err:
        current_app.logger.error('Update Failed:', err.with_traceback(None))
        return -1
