"""Database service for retrieving bad names from the data source."""

from cloud_sql_connector import DBConfig, getconn
from flask import current_app

from .utils import get_yesterday_utc_range


def get_bad_names() -> list[dict]:
    """
    Fetch bad names from the database and return as a list of dictionaries.

    A "bad name" is defined as:
      - In 'NE' state
      - Not associated with approved or conditional names
      - Contains non-standard ASCII characters
      - Event occurred after the start of yesterday UTC
    """
    schema = current_app.config.get("DB_SCHEMA", "public")

    db_config = DBConfig(
        instance_name=current_app.config.get("DB_INSTANCE_CONNECTION_NAME"),
        database=current_app.config.get("DB_NAME"),
        user=current_app.config.get("DB_USER"),
        ip_type=current_app.config.get("DB_IP_TYPE", "private"),
        schema=schema,
        pool_recycle=300,
    )

    # Ensure required fields are set
    if not all([db_config.instance_name, db_config.database, db_config.user]):
        raise ValueError(
            "DBConfig fields instance_name, database, and user must be set"
        )

    conn = getconn(db_config)
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
