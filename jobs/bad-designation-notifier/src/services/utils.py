from datetime import datetime, timedelta
import pytz

# Column definitions: (Key, Header, Width)
# Column definitions: (Key, Header)
columns = [
    ("event_time", "EVENT TIME"),
    ("nr_num", "NR NUM"),
    ("name", "NAME"),
    ("entity_type_cd", "ENTITY_TYPE"),
    ("status", "STATUS"),
    ("consumed_date", "CONSUMED_DATE"),
    ("consumed_by", "CONSUMED BY")
]

# Extract only the keys and headers
column_keys = [col[0] for col in columns]
column_headers = [col[1] for col in columns]

def get_yesterday_str():
    """Returns yesterday's date in 'yyyy-mm-dd' format based on Pacific Time."""
    pacific = pytz.timezone('America/Los_Angeles')

    # Get current UTC time and convert to Pacific Time
    now_utc = datetime.now(tz=pytz.utc)
    now_pacific = now_utc.astimezone(pacific)

    # Calculate yesterday's date
    start_of_yesterday = now_pacific - timedelta(days=1)
    
    # Format the date as yyyy-mm-dd
    return start_of_yesterday.strftime('%Y-%m-%d')
