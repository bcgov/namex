import csv, os, psycopg2
from dotenv import load_dotenv, find_dotenv

"""
This is a utility find all NRs with state COMPLETED, and convert to APPROVED, CONDITIONAL, or 
REJECTED based on the state of the names of the NR.
"""

load_dotenv(find_dotenv())

print('***')

# get db connection settings from environment variables
DB_USER = os.getenv('DATABASE_USERNAME', '')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
DB_NAME = os.getenv('DATABASE_NAME', '')
DB_HOST = os.getenv('DATABASE_HOST', '')
DB_PORT = os.getenv('DATABASE_PORT', '5432')

pg_conn = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}' port='{4}'".
                           format(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT))

# make sure PG is doing the right level of transaction management
#pg_conn.set_session(isolation_level='REPEATABLE READ', readonly=False, deferrable=False, autocommit=False)
pg_cur = pg_conn.cursor()
pg_cur_names = pg_conn.cursor()
pg_cur_update = pg_conn.cursor()

# find and loop through all COMPLETED NRs
pg_cur.execute("select * from requests where state_cd = 'COMPLETED'")

for row in pg_cur:

    nr_id = row[0]
    new_state = None

    print(nr_id)


    # find and loop through all names for this NR
    pg_cur_names.execute("select * from names where nr_id = {}".format(row[0]))

    for name in pg_cur_names:

        name_state = name[2]

        print("  {}".format(name_state))

        # same logic as in extractor
        if new_state in [None, 'REJECTED'] and name_state == 'APPROVED':
            new_state = 'APPROVED'
        elif new_state in [None, 'REJECTED', 'APPROVED'] and name_state == 'CONDITION':
            new_state = 'CONDITIONAL'
        elif new_state == None and name_state == 'REJECTED':
            new_state = 'REJECTED'

    print("  new state: {}".format(new_state))

    # update NR state
    if new_state is not None:
        pg_cur_update.execute("update requests set state_cd = '{}' where id={}".format(new_state, nr_id))
        pg_conn.commit()

# commit all changes
print("ALL DONE")



