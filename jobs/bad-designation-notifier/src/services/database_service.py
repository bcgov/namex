from flask import current_app
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config import get_named_config
from .utils import get_yesterday_str

config = get_named_config

def get_bad_designations():
    """Fetches bad names from the database."""
    # Create the database engine and session
    engine = create_engine(current_app.config["NAMEX_DATABASE_URI"])
    Session = sessionmaker(bind=engine)
    session = Session()

    yesterday_pacific = get_yesterday_str()

    # Print the timestamps
    current_app.logger.info(f"Yesterday (Pacific): {yesterday_pacific}")

    try:
        # Wrap the query in text()
        query = text(f"""
          select
          r.nr_num
          ,n.name
          ,TO_CHAR(r.last_update AT TIME ZONE 'America/Vancouver', 'YYYY-MM-DD HH24:MI:SS') AS last_update
          ,r.request_type_cd
          ,r.entity_type_cd
          ,r.state_cd
          ,TO_CHAR(r.expiration_date, 'YYYY-MM-DD HH24:MI:SS') AS expiration_date
          ,n.corp_num as consumed_corp_num
          ,TO_CHAR(n.consumption_date AT TIME ZONE 'America/Vancouver', 'YYYY-MM-DD HH24:MI:SS') AS consumed_date
          from requests r
          ,names n
          where r.id=n.nr_id
          and to_char(last_update at time zone 'America/Vancouver','yyyy-mm-dd') = '{yesterday_pacific}'
          and r.request_type_cd in ('FR','LL','LP','XLL','XLP')
          and r.state_cd NOT in ('CANCELLED','EXPIRED','PENDING_DELETION','REJECTED')
          and
          (
          replace(name,'.','') like '%CCC'
          or replace(name,'.','') like '%COMMUNITY CONTRIBUTION COMPANY'
          or replace(name,'.','') like '%CORP'
          or replace(name,'.','') like '%CORPORATION'
          or replace(name,'.','') like '%INC'
          or replace(name,'.','') like '%INCORPORATED'
          or replace(name,'.','') like '%INCORPOREE'
          or (replace(name,'.','') like '%LIMITED' and replace(name,'.','') not like '%UNLIMITED')
          or replace(name,'.','') like '%LIMITEE'
          or replace(name,'.','') like '%LIMITED LIABILITY COMPANY'
          or replace(name,'.','') like '%LIMITED LIABILITY CO'
          or replace(name,'.','') like '%LLC'
          or replace(name,'.','') like '%LTEE'
          or replace(name,'.','') like '%LTD'
          or replace(name,'.','') like '%SRI'
          or replace(name,'.','') like '%ULC'
          or replace(name,'.','') like '%UNLIMITED LIABILITY COMPANY'
          )
          and r.nr_num not like 'NR L%'
          order by r.last_update desc
        """)
        result = session.execute(query).fetchall()

        # Convert result rows to a list of dictionaries
        keys = ["nr_num","name", "last_update", "request_type_cd", "entity_type_cd", "state_cd", "expiration_date", "consumed_corp_num", "consumed_date"]
        formatted_result = [
            [(value if value is not None else 'n/a') for value in row]
            for row in result
        ]

        return formatted_result
    finally:
        # Ensure the session is closed
        session.close()