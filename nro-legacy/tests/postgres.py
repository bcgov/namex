import os
import psycopg2

class Postgres(object):

    def __init__(self):
        self.database = os.environ['PGDATABASE']
        self.user = os.environ['PGUSER']
        self.password = os.environ['PGPASSWORD']

    def execute(self, sql, values=()):
        with psycopg2.connect(host='localhost',dbname=self.database, user=self.user, password=self.password) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, values)

    def selectFirst(self, sql):
        with psycopg2.connect(host='localhost',dbname=self.database, user=self.user, password=self.password) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchone()
