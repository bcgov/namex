from namex.utils.logging import setup_logging
setup_logging() ## important to do this first

from nro.app import create_app, db
from datetime import datetime
import cx_Oracle
import sys
from flask import current_app
from config import Config
from namex.models import Request

def get_ops_params():
    try:
        max_rows = int(current_app.config.get('MAX_ROW_LIMIT', 100))
    except:
        max_rows = 100


    return max_rows


# #### Get extra decision data (decision text, conflicts) from NRO for completed NRs
# #########################################

# this allows me to use the NameX ORM Model, and use the db scoped session attached to the models.
app = create_app(Config)
max_rows = get_ops_params()

start_time = datetime.utcnow()
row_count = 0

def job_result_set(ora_con, max_rows):

    ora_cursor = ora_con.cursor()

    result_set = ora_cursor.execute("""
        SELECT ID, NR_NUM, STATUS
        FROM namex.namex_datafix
        where status != 'COMPLETE' AND rownum <= :max_rows
        """
                                , max_rows=max_rows
                                )
    col_names = [row[0] for row in ora_cursor.description]

    return result_set, col_names

def update_datafix_row(ora_con, id, status):

    try:
        ora_cursor = ora_con.cursor()

        result_set = ora_cursor.execute("""
            update NAMEX.NAMEX_DATAFIX 
			set STATUS = :status
            where id = :id
            """
            ,id=id
        )

        print('rows updated',ora_cursor.rowcount)
        if ora_cursor.rowcount > 0:
            return True
    except Exception as err:
        current_app.logger.error('UNABLE TO UPDATE NAMEX_DATAFIX :', err.with_traceback(None))

    return False

try:

    ora_con = cx_Oracle.connect(Config.ORA_USER,
                                Config.ORA_PASSWORD,
                                "{0}:{1}/{2}".format(Config.ORA_HOST, Config.ORA_PORT, Config.ORA_NAME))

    result, col_names = job_result_set(ora_con, max_rows)

   

    for r in result:
        row_count += 1

        row = ora_row_to_dict(col_names, r)

        nr_num = row['nr_num']
        nr = Request.find_by_nr(nr_num)
		
		current_app.logger.debug('processing: {}, NameX state: {}'
                                     .format(
                nr_num,
                None if (not nr) else nr.stateCd
            ))

        try:
            nr = nro.fetch_nro_request_and_copy_to_namex_request(user, nr_number=nr_num, name_request=nr)
            namex_db.session.add(nr)
            EventRecorder.record(user, Event.UPDATE_FROM_NRO, nr, {}, save_to_session=True)
            current_app.logger.debug('EventRecorder should have been saved to by now, although not committed')

            success = update_datafix_row(ora_con
                                            , id=row['id']
                                            , status='COMPLETE'
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
                                            , status='ERROR'
                                            )
                namex_db.session.rollback()
                ora_con.commit()

        return row_count



except Exception as err:
    db.session.rollback()

    print('NRO Update Failed:', err, err.with_traceback(None), file=sys.stderr)

    exit(1)


finally:
    if 'ora_con' in locals() and ora_con:
        ora_con.close()

app.do_teardown_appcontext()
end_time = datetime.utcnow()
print("job - requests processed: {0} completed in:{1}".format(row_count, end_time-start_time))
exit(0)

