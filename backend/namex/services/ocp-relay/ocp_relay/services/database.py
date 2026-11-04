import cx_Oracle
from sqlalchemy import create_engine

from config import Config


# Oracle - Colin
def get_colin_connection():
    dsn = cx_Oracle.makedsn(host=Config.COLIN_HOST, port=Config.COLIN_PORT, service_name=Config.COLIN_DB_NAME)
    return cx_Oracle.connect(user=Config.COLIN_USER, password=Config.COLIN_PASSWORD, dsn=dsn)


# Postgres - Pay
PAY_DATABASE_URI = Config.PAY_SQLALCHEMY_DATABASE_URI
pay_sql_engine = create_engine(PAY_DATABASE_URI)
