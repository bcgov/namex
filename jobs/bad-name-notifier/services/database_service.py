from flask import current_app
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import get_named_config
from .utils import get_yesterday_utc_range

config = get_named_config

def get_bad_names():
    """Fetches bad names from the database."""
    # Create the database engine and session
    engine = create_engine(current_app.config["NAMEX_DATABASE_URI"])
    Session = sessionmaker(bind=engine)
    session = Session()

    start_of_yesterday_utc, start_of_today_utc = get_yesterday_utc_range()

    # Print the timestamps
    current_app.logger.info("Start of yesterday (UTC):", start_of_yesterday_utc)
    current_app.logger.info("Start of today (UTC):", start_of_today_utc)

    try:
        # Wrap the query in text()
        query = text(f"""
        SELECT DISTINCT r.nr_num, n.choice, n.name
        FROM requests r
        JOIN names n ON r.id = n.nr_id
        JOIN events e on r.id = e.nr_id
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
          --AND e.event_dt < '{start_of_today_utc}'
        """)
        result = session.execute(query).fetchall()

        # Convert result rows to a list of dictionaries
        keys = ["nr_num", "choice", "name"]
        formatted_result = [dict(zip(keys, row)) for row in result]

        return formatted_result
    finally:
        # Ensure the session is closed
        session.close()