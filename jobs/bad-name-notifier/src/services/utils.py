from datetime import datetime, timedelta
import pytz

def get_yesterday_str():
        # Calculate yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    
    # Format the date as yyyy-mm-dd
    formatted_date = yesterday.strftime('%Y-%m-%d')

def get_yesterday_utc_range():
    pacific = pytz.timezone('America/Los_Angeles')

    # Calculate the start of today and yesterday in Pacific Time
    start_of_today_pacific = pacific.localize(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    start_of_yesterday_pacific = start_of_today_pacific - timedelta(days=1)

    # Convert to UTC
    start_of_today_utc = start_of_today_pacific.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
    start_of_yesterday_utc = start_of_yesterday_pacific.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')

    return start_of_yesterday_utc, start_of_today_utc