from flask import current_app
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import get_named_config
from .utils import get_yesterday_str, column_keys
from namex.constants import EntityTypeDescriptions, EntityTypes

config = get_named_config

# Create a dictionary that maps entity type codes (values) to their string keys (attribute names)
entity_type_lookup = {v.value: k.replace("_", " ").title() for k, v in EntityTypes.__members__.items()}  # Enum case

def get_bad_designations():
    """Fetches bad names from the database and formats them for email output."""
    # Create the database engine and session
    engine = create_engine(current_app.config["NAMEX_DATABASE_URI"])
    session = sessionmaker(bind=engine)()

    yesterday_pacific = get_yesterday_str()

    # Print the timestamps
    current_app.logger.info(f"Yesterday (Pacific): {yesterday_pacific}")

    try:
        # SQL Query
        query = text(f"""
          select
            TO_CHAR(r.last_update AT TIME ZONE 'America/Vancouver', 'DD-MON-YY HH24:MI:SS') AS event_time,
            r.nr_num,
            n.name,
            r.entity_type_cd,
            --n.choice,
            r.state_cd,
            --TO_CHAR(r.expiration_date AT TIME ZONE 'America/Vancouver', 'DD-MON-YY HH24:MI:SS') AS expiration_date,
            TO_CHAR(n.consumption_date AT TIME ZONE 'America/Vancouver', 'DD-MON-YY HH24:MI:SS') AS consumed_date,
            n.corp_num as consumed_by
          from requests r
          join names n on r.id=n.nr_id
          where to_char(r.last_update at time zone 'America/Vancouver','yyyy-mm-dd') = '{yesterday_pacific}'
          and r.request_type_cd in ('FR','LL','LP','XLL','XLP')
          and r.state_cd NOT in ('CANCELLED','EXPIRED','PENDING_DELETION','REJECTED')
          and (
              replace(n.name,'.','') like '%CCC'
              or replace(n.name,'.','') like '%COMMUNITY CONTRIBUTION COMPANY'
              or replace(n.name,'.','') like '%CORP'
              or replace(n.name,'.','') like '%CORPORATION'
              or replace(n.name,'.','') like '%INC'
              or replace(n.name,'.','') like '%INCORPORATED'
              or replace(n.name,'.','') like '%INCORPOREE'
              or (replace(n.name,'.','') like '%LIMITED' and replace(n.name,'.','') not like '%UNLIMITED')
              or replace(n.name,'.','') like '%LIMITEE'
              or replace(n.name,'.','') like '%LIMITED LIABILITY COMPANY'
              or replace(n.name,'.','') like '%LIMITED LIABILITY CO'
              or replace(n.name,'.','') like '%LLC'
              or replace(n.name,'.','') like '%LTEE'
              or replace(n.name,'.','') like '%LTD'
              or replace(n.name,'.','') like '%SRI'
              or replace(n.name,'.','') like '%ULC'
              or replace(n.name,'.','') like '%UNLIMITED LIABILITY COMPANY'
          )
          and r.nr_num not like 'NR L%'
          order by r.last_update desc
        """)

        results =  session.execute(query).fetchall()

        # Convert result rows to a list of dictionaries (more readable!)
        formatted_results = [
            {
                key: (
                    entity_type_lookup.get(value, value) if key == "entity_type_cd"
                    else (value if value is not None else 'n/a')
                )
                for key, value in zip(column_keys, row)
            }
            for row in results
        ]
        return formatted_results
    finally:
        session.close()
