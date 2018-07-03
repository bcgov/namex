from __future__ import print_function
from datetime import datetime
from config import Config

import cx_Oracle
import psycopg2
import psycopg2.extras

# connect to both databases
ora_con = cx_Oracle.connect(Config.ORA_USER,
                            Config.ORA_PASSWORD,
                            "{0}:{1}/{2}".format(Config.ORA_HOST, Config.ORA_PORT, Config.ORA_NAME))

pg_conn = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}' port='{4}'".
                           format(Config.PG_HOST, Config.PG_NAME, Config.PG_USER, Config.PG_PASSWORD, Config.PG_PORT))

# make sure PG is doing the right level of transaction management
pg_conn.set_session(isolation_level='REPEATABLE READ', readonly=False, deferrable=False, autocommit=False)

start_time = datetime.utcnow()

pg_cur = pg_conn.cursor()

pg_cur.execute("select nextval('nro_job_seq');")
job_id = pg_cur.fetchone()[0]
state = 'running'

pg_cur.execute("""insert into nro_names_sync_job (id, status_cd, start_time) values (%s, %s, %s);""",
               (job_id, state, start_time))
pg_conn.commit()

try:

    ora_con.begin()
    ora_cursor = ora_con.cursor()

    pg_cur_track = pg_conn.cursor()

    pg_upd_cursor = pg_conn.cursor()

    pg_cursor = pg_conn.cursor('serverside_cursor_sel_nro', cursor_factory=psycopg2.extras.DictCursor)
    pg_cursor.execute("SELECT * " +
                      ",(SELECT username FROM users WHERE id=r.user_id) as username " +
                      ",(last_update::date + integer '60') as expiry_date " +
                      "FROM requests r " +
                      "WHERE state_cd in ('APPROVED', 'REJECTED', 'CONDITIONAL') " +
                      "  AND last_update <= current_timestamp - (%s ||' minutes')::interval "
                      "  AND (furnished != 'Y' " +
                      "       OR furnished is NULL) " +
                      " FOR UPDATE "
                      "LIMIT %s",
                      [Config.MIN_DELAY_MINUTES, Config.MAX_ROW_LIMIT]
                      )

    row_count = 0
    for pg_row in pg_cursor:
        row_count += 1

        try:
            # set consent flag if this NR was conditionally accepted
            if pg_row['state_cd'] == 'CONDITIONAL':
                pg_row['consent_flag'] = 'Y'
            else:
                pg_row['consent_flag'] = 'N'

            # intialize p_choice* (decision text) fields
            p_choice1 = ''
            p_choice2 = ''
            p_choice3 = ''

            # create stub array for up to three name choices
            names = [
                {
                    'conflict1': '',
                    'conflict2': '',
                    'conflict3': '',
                },
                {
                    'conflict1': '',
                    'conflict2': '',
                    'conflict3': '',
                },
                {
                    'conflict1': '',
                    'conflict2': '',
                    'conflict3': '',
                },
            ]

            ### iterate through name data

            # reset the cursor from the previous loop run
            try:
                pg_cursor_names.close()
            except:
                pass

            # get the names associated with this NR
            pg_cursor_names = pg_conn.cursor('serverside_cursor_sel_names', cursor_factory=psycopg2.extras.RealDictCursor)
            names_sql = "select * from names where nr_id = " + str(pg_row['id']) + " order by choice"
            pg_cursor_names.execute(names_sql)

            for name in pg_cursor_names:
                # change name state from C (conditional) to A (accept) - we only send A or R, or NE for not examined
                if name['state'] == 'C':
                    name['state'] = 'A'

                # build decision text for proc from status and message (max 1000 chars)
                decision_text = ''
                if name['state'] in ['A', 'R']:
                    decision_text = '{}****{}'.format(name['state'], name['decision_text'])[:1000]

                # format conflicts as <conflict number>****<conflict name>

                if name['conflict1'] in (None, ''): name['conflict1'] = ''
                else: name['conflict1'] = '{}****{}'.format(name['conflict1_num'], name['conflict1'][:150])

                if name['conflict2'] in (None, ''): name['conflict2'] = ''
                else: name['conflict2'] = '{}****{}'.format(name['conflict2_num'], name['conflict2'][:150])

                if name['conflict3'] in (None, ''): name['conflict3'] = ''
                else: name['conflict3'] = '{}****{}'.format(name['conflict3_num'], name['conflict3'][:150])


                # save off data for use in proc call below
                if name['choice'] == 1:
                    p_choice1 = decision_text
                    names[0] = name
                if name['choice'] == 2:
                    p_choice2 = decision_text
                    names[1] = name
                if name['choice'] == 3:
                    p_choice3 = decision_text
                    names[2] = name


            ### Call the name_examination procedure to save complete decision data for a single NR
            ora_cursor.callproc("NRO_DATA_PUMP_PKG.name_examination",
                                    [pg_row['nr_num'],        #p_nr_number
                                     pg_row['state_cd'],      #p_status
                                     pg_row['expiry_date'],   #p_expiry_date
                                     pg_row['consent_flag'],  #p_consent_flag
                                     pg_row['username'],      #p_examiner_id
                                     p_choice1,               #p_choice1
                                     p_choice2,               #p_choice2
                                     p_choice3,               #p_choice3
                                     '',                      #p_exam_comment ???
                                     '',                      #p_add_info ???
                                     names[0]['conflict1'],
                                     names[0]['conflict2'],
                                     names[0]['conflict3'],
                                     names[1]['conflict1'],
                                     names[1]['conflict2'],
                                     names[1]['conflict3'],
                                     names[2]['conflict1'],
                                     names[2]['conflict2'],
                                     names[2]['conflict3'],
                                     ]
                                )

            pg_upd_cursor.execute("""UPDATE requests SET furnished = %s WHERE id = %s""",
                                  ['Y', pg_row['id']])

            pg_cur_track.execute(
                """insert into nro_names_sync_job_detail (job_id, nr_num, time) values (%s, %s, %s);""",
                (job_id, pg_row['nr_num'], datetime.utcnow()))

        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print("NR#:", pg_row['nr_num'], "Oracle-Error-Code:", error.code)
            # print("Oracle-Error-Message:", error.message)
        except Exception as err:
            print("NR#:", pg_row['nr_num'], "Error:", err)

    # update the tracking status
    end_time = datetime.utcnow()
    state = 'success'
    pg_cur.execute("""update nro_names_sync_job set status_cd =%s, end_time=%s where id=%s;""",
                   (state, end_time, job_id))

    # commit and save the changes
    ora_con.commit()
    pg_conn.commit()

except Exception as err:
    # something went wrong, roll it all back
    #TODO: Notify ops of the error in sync
    print ('Exception:', err)
    ora_con.rollback()
    pg_conn.rollback()

finally:
    if ora_con is not None:
        ora_con.close()

    if pg_conn is not None:
        pg_conn.close()

print("job - requests processed: {0} completed in:{1}".format(row_count, end_time-start_time))
