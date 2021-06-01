from flask import Flask, g, current_app
from flask_marshmallow import Marshmallow
from config import Config

from namex import db
from namex.services import EventRecorder
from namex.services.nro import NROServices
from namex.services.nro.utils import ora_row_to_dict
from namex.models import Request, Event, State

from extractor.utils.logging import setup_logging


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
        SELECT ID, NR_NUM, STATUS, ACTION, SEND_COUNT, SEND_TIME, ERROR_MSG
         FROM (
            SELECT *
            FROM namex.namex_feeder
            WHERE status in ('E', 'P')
            ORDER BY id
            )
            where rownum <= :max_rows
        """
                                , max_rows=max_rows
                                )
    col_names = [row[0] for row in ora_cursor.description]

    return result_set, col_names


def update_feeder_row(ora_con, id, status, send_count, error_message):

    try:
        ora_cursor = ora_con.cursor()

        result_set = ora_cursor.execute("""
            update NAMEX.NAMEX_FEEDER set
            STATUS = :status
            ,SEND_COUNT = :send_count
            ,SEND_TIME = sysdate
            ,ERROR_MSG = :error_message
            where id = :id
            """
                                        ,id=id
                                        ,status=status
                                        ,send_count=send_count
                                        ,error_message=error_message
                                    )

        print('rows updated',ora_cursor.rowcount)
        if ora_cursor.rowcount > 0:
            return True
    except Exception as err:
        current_app.logger.error('UNABLE TO UPDATE NAMEX_FEEDER :', err.with_traceback(None))

    return False


def job(app, namex_db, nro_connection, user, max_rows=100):

    row_count = 0

    try:
        ora_con = nro_connection
        result, col_names = job_result_set(ora_con, max_rows)

        for r in result:

            row_count += 1

            row = ora_row_to_dict(col_names, r)

            nr_num = row['nr_num']
            nr = Request.find_by_nr(nr_num)
            action = row['action']

            current_app.logger.debug('processing: {}, NameX state: {}, action: {}'
                                     .format(
                nr_num,
                None if (not nr) else nr.stateCd,
                action
            ))

            if nr and (nr.stateCd not in [State.DRAFT, State.PENDING_PAYMENT]):

                # do NOT ignore updates of completed NRs, since those are CONSUME transactions -
                # the only kind that gets into the namex_feeder table for completed NRs
                if nr.stateCd in State.COMPLETED_STATE and action == 'U':
                    pass

                elif action != 'X':
                    success = update_feeder_row(ora_con
                                                ,id=row['id']
                                                ,status='C'
                                                ,send_count=1 + 0 if (row['send_count'] is None) else row['send_count']
                                                , error_message='Ignored - Request: not processed')
                    ora_con.commit()
                    continue
            # prevent new NRs from namerequest going through here
            if not nr or (nr and nr.stateCd not in [State.DRAFT, State.PENDING_PAYMENT]):
                try:
                    nr = nro.fetch_nro_request_and_copy_to_namex_request(user, nr_number=nr_num, name_request=nr)

                    namex_db.session.add(nr)
                    EventRecorder.record(user, Event.UPDATE_FROM_NRO, nr, nr.json(), save_to_session=True)
                    current_app.logger.debug('EventRecorder should have been saved to by now, although not committed')

                    success = update_feeder_row(ora_con
                                                , id=row['id']
                                                , status='C'
                                                , send_count=1 + 0 if (row['send_count'] is None) else row['send_count']
                                                , error_message=None)

                    if success:
                        ora_con.commit()
                        current_app.logger.debug('Oracle commit done')
                        namex_db.session.commit()
                        current_app.logger.debug('Postgresql commit done')
                    else:
                        raise Exception()

                except Exception as err:
                    current_app.logger.error(err.with_traceback(None))
                    success = update_feeder_row(ora_con
                                                , id=row['id']
                                                , status=row['status']
                                                , send_count=1 + 0 if (row['send_count'] is None) else row['send_count']
                                                , error_message=err.with_traceback(None))
                    namex_db.session.rollback()
                    ora_con.commit()

        return row_count

    except Exception as err:
        current_app.logger.error('Update Failed:', err.with_traceback(None))
        return -1
