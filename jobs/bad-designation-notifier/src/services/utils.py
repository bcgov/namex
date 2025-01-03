from datetime import datetime, timedelta
import pytz

def get_yesterday_str():
    pacific = pytz.timezone('America/Los_Angeles')

    # Calculate the start of today and yesterday in Pacific Time
    start_of_today_pacific = pacific.localize(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    start_of_yesterday_pacific = start_of_today_pacific - timedelta(days=1)

    # Format the date as yyyy-mm-dd
    return start_of_yesterday_pacific.strftime('%Y-%m-%d')