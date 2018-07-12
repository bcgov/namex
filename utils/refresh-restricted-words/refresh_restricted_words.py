import csv, os, psycopg2

"""
This is a utility to take a set of three CSV files off the server and replace existing Restricted Words data with contents.
:return: static text, error messaging or "done" 

Expects two spreadsheets in the same directory:
restricted_word.csv - list of words
restricted_condition.csv - list of conditions with cross-reference to words 
"""

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
pg_conn.set_session(isolation_level='REPEATABLE READ', readonly=False, deferrable=False, autocommit=False)
pg_cur = pg_conn.cursor()


# delete all records in cross-reference table, then words and conditions tables
pg_cur.execute("TRUNCATE restricted_word_condition")
pg_cur.execute("TRUNCATE restricted_word")
pg_cur.execute("TRUNCATE restricted_condition")


# add new words
with open('restricted_word.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        pg_cur.execute("insert into restricted_word values ({}, '{}')".format(row['word_id'], row['word_phrase']))
        pg_conn.commit()

# add new conditions and cross-reference records
with open('restricted_condition.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            pg_cur.execute("insert into restricted_condition values ({}, '{}', '{}', '{}', '{}', '{}')".format(
                row['cnd_id'],
                row['Examiner Information (cnd_text)'].replace("'", "''"),
                row['allow_use'],
                row['consent_required'],
                row['consenting_body'].replace("'", "''"),
                row['Formatted Client Instructions (instructions)'].replace("'", "''"),
            ))
            # commit after each insert so we don't run out of cache? limited number of conditions were added when we
            # left the commit to the end
            pg_conn.commit()

        except psycopg2.IntegrityError as e:
            # duplicate ID
            pg_conn.rollback()


        # add cross-reference records
        try:
            pg_cur.execute("insert into restricted_word_condition values ({}, {})".format(
                row['cnd_id'],
                row['word_id'],
            ))
            pg_conn.commit()

        except psycopg2.IntegrityError as e:
            # duplicate ID
            pg_conn.rollback()

# commit all changes
pg_conn.commit()
print("done")



