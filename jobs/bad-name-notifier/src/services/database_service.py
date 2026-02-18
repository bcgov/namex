"""Database service for retrieving bad names from the data source."""

from flask import current_app
from google.cloud.sql.connector import Connector

from .utils import get_yesterday_utc_range


def getconn():
    """Create and return a database connection using Cloud SQL Connector.
    Returns:
        tuple: A tuple containing (connection, connector instance).
    """
    connector = Connector()
    conn = connector.connect(
        current_app.config.get("DB_INSTANCE_CONNECTION_NAME"),
        "pg8000",  # driver
        user=current_app.config.get("DB_USER"),
        db=current_app.config.get("DB_NAME"),
        ip_type=current_app.config.get("DB_IP_TYPE", "private"),
        enable_iam_auth=True,  # 🔥 REQUIRED
    )
    return conn, connector


def get_bad_names() -> list[dict]:
    """
    Fetch bad names from the database and return as a list of dictionaries.

    A "bad name" is defined as:
      - In 'NE' state
      - Not associated with approved or conditional names
      - Contains non-standard ASCII characters
      - Event occurred after the start of yesterday UTC
    """
    conn, connector = getconn()
    cursor = conn.cursor()

    start_of_yesterday_utc, start_of_today_utc = get_yesterday_utc_range()
    current_app.logger.info(f"Start of yesterday (UTC): {start_of_yesterday_utc}")
    current_app.logger.info(f"Start of today (UTC): {start_of_today_utc}")

    sql = f"""
        SELECT DISTINCT r.nr_num, n.choice, n.name
        FROM requests r
        JOIN names n ON r.id = n.nr_id
        JOIN events e ON r.id = e.nr_id
        WHERE n.state = 'NE'
          AND r.nr_num NOT LIKE 'NR L%'
          AND NOT EXISTS (
            SELECT 1
            FROM names n2
            WHERE n2.nr_id = r.id
              AND n2.state IN ('APPROVED', 'CONDITION')
          )
          AND EXISTS (
            SELECT 1
            FROM generate_series(1, length(n.name)) AS i
            WHERE ascii(substr(n.name, i, 1)) < 32
               OR ascii(substr(n.name, i, 1)) > 122
          )
          AND e.event_dt >= '{start_of_yesterday_utc}'
          -- AND e.event_dt < '{start_of_today_utc}'
        ORDER BY r.nr_num
    """

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Map results to a list of dicts
        keys = ["nr_num", "choice", "name"]
        formatted = [dict(zip(keys, row)) for row in rows]

        return formatted

    finally:
        cursor.close()
        conn.close()
        connector.close()
