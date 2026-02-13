"""Database service module for querying bad corporate designations."""

from flask import current_app
from google.cloud.sql.connector import Connector
from namex.constants import EntityTypes

from .utils import column_keys, get_yesterday_str

# Map entity type codes to human-readable names
entity_type_lookup = {
    v.value: k.replace(
        "_",
        " ").title() for k,
    v in EntityTypes.__members__.items()}


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


def get_bad_designations():
    """Fetch bad names from the database and return as list of dicts."""

    conn, connector = getconn()
    cursor = conn.cursor()

    yesterday_pacific = get_yesterday_str()
    current_app.logger.info(f"Yesterday (Pacific): {yesterday_pacific}")

    sql = f"""
        SELECT
            TO_CHAR(r.last_update AT TIME ZONE 'America/Vancouver', 'DD-MON-YY HH24:MI:SS') AS event_time,
            r.nr_num,
            n.name,
            r.entity_type_cd,
            r.state_cd,
            TO_CHAR(n.consumption_date AT TIME ZONE 'America/Vancouver', 'DD-MON-YY HH24:MI:SS') AS consumed_date,
            n.corp_num AS consumed_by
        FROM requests r
        JOIN names n ON r.id = n.nr_id
        WHERE to_char(r.last_update AT TIME ZONE 'America/Vancouver',
                     'yyyy-mm-dd') = '{yesterday_pacific}'
        AND r.request_type_cd IN ('FR','LL','LP','XLL','XLP')
        AND r.state_cd NOT IN ('CANCELLED','EXPIRED','PENDING_DELETION','REJECTED')
        AND (
            replace(n.name,'.','') LIKE '%CCC'
            OR replace(n.name,'.','') LIKE '%COMMUNITY CONTRIBUTION COMPANY'
            OR replace(n.name,'.','') LIKE '%CORP'
            OR replace(n.name,'.','') LIKE '%CORPORATION'
            OR replace(n.name,'.','') LIKE '%INC'
            OR replace(n.name,'.','') LIKE '%INCORPORATED'
            OR replace(n.name,'.','') LIKE '%INCORPOREE'
            OR (replace(n.name,'.','') LIKE '%LIMITED' AND replace(n.name,'.','') NOT LIKE '%UNLIMITED')
            OR replace(n.name,'.','') LIKE '%LIMITEE'
            OR replace(n.name,'.','') LIKE '%LIMITED LIABILITY COMPANY'
            OR replace(n.name,'.','') LIKE '%LIMITED LIABILITY CO'
            OR replace(n.name,'.','') LIKE '%LLC'
            OR replace(n.name,'.','') LIKE '%LTEE'
            OR replace(n.name,'.','') LIKE '%LTD'
            OR replace(n.name,'.','') LIKE '%SRI'
            OR replace(n.name,'.','') LIKE '%ULC'
            OR replace(n.name,'.','') LIKE '%UNLIMITED LIABILITY COMPANY'
        )
        AND r.nr_num NOT LIKE 'NR L%'
        ORDER BY r.last_update DESC
    """

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()

        formatted = []
        for row in rows:
            entry = {}
            for key, value in zip(column_keys, row):
                if key == "entity_type_cd":
                    entry[key] = entity_type_lookup.get(value, value)
                else:
                    entry[key] = value if value is not None else "n/a"
            formatted.append(entry)

        return formatted

    finally:
        cursor.close()
        conn.close()
        connector.close()
