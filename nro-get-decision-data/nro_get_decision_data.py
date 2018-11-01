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


def get_names_from_nro(ora_cursor, nr_num):
    # get the NR Names
    #############################
    sql = "select choice_number, name, state_comment, conflict_1_number, conflict_1_name, " \
          "conflict_2_number, conflict_2_name, conflict_3_number, conflict_3_name  " \
          "from names_with_decisions_vw where nr_num = :nr_num"
    result = ora_cursor.execute(sql, {'nr_num': str(nr_num)})
    names = []
    for row in result:
        names.append({
            'choice_number': row[0],
            'name': row[1],
            'state_comment': row[2],
            'conflict_1_number': row[3],
            'conflict_1_name': row[4],
            'conflict_2_number': row[5],
            'conflict_2_name': row[6],
            'conflict_3_number': row[7],
            'conflict_3_name': row[8],
        })
    if len(names) < 1:
        return None
    return names


# #### Get extra decision data (decision text, conflicts) from NRO for completed NRs
# #########################################

# this allows me to use the NameX ORM Model, and use the db scoped session attached to the models.
app = create_app(Config)
max_rows = get_ops_params()

start_time = datetime.utcnow()
row_count = 0

try:

    ora_con = cx_Oracle.connect(Config.ORA_USER,
                                Config.ORA_PASSWORD,
                                "{0}:{1}/{2}".format(Config.ORA_HOST, Config.ORA_PORT, Config.ORA_NAME))

    ora_cursor = ora_con.cursor()

    # get list of NRs that need to be processed
    r_query = db.engine.execute("select nr_num from get_decision_data_table_tracker "
                                "where success is NULL "
                                "FETCH FIRST {} ROWS ONLY".format(max_rows))
    records = r_query.fetchall()

    for nr_num in records:
        nr_num = nr_num[0]
        current_app.logger.info(nr_num)

        # get NR
        nr = Request.find_by_nr(nr_num)

        # if there is no NR in Namex for this NR, log issue in table
        if not nr:
            db.engine.execute("update get_decision_data_table_tracker "
                                          "set success=false, message='{}'"
                                          "where nr_num = '{}'"
                                          .format("NR not found in Namex [1]", nr_num))
            continue

        try:

            # get name data from NRO
            nro_names = get_names_from_nro(ora_cursor, nr_num)

            if not nro_names:
                # log error in table
                db.engine.execute("update get_decision_data_table_tracker "
                                  "set success=false, message='{}'"
                                  "where nr_num = '{}'"
                                  .format("NRO could not find names for this NR [3]", nr_num))
                continue


            # update NR with data - keep last update date as is
            namex_names = nr.names.all()
            for nro_name in nro_names:
                for namex_name in namex_names:
                    if namex_name.choice == nro_name['choice_number']:
                        namex_name.decision_text = nro_name['state_comment']
                        namex_name.conflict1 = nro_name['conflict_1_name']
                        namex_name.conflict2 = nro_name['conflict_2_name']
                        namex_name.conflict3 = nro_name['conflict_3_name']
                        namex_name.conflict1_num = nro_name['conflict_1_number']
                        namex_name.conflict2_num = nro_name['conflict_2_number']
                        namex_name.conflict3_num = nro_name['conflict_3_number']

                        #namex_name.save()

                        db.session.add(namex_name)
            db.session.commit()




            # update status in processing table
            db.engine.execute("update get_decision_data_table_tracker "
                                          "set success=true, message='{}'"
                                          "where nr_num = '{}'"
                                          .format("", nr_num))
            row_count += 1

        except Exception as err:
            current_app.logger.error(err)
            current_app.logger.error('ERROR: {}'.format(nr.nrNum))
            db.session.rollback()

            # log error in table
            db.engine.execute("update get_decision_data_table_tracker "
                                          "set success=false, message='{}'"
                                          "where nr_num = '{}'"
                                          .format("{} [2]".format(str(err)), nr_num))




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

