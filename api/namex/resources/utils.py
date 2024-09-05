import re
from datetime import datetime


class DateUtils:
    # Regex patterns to match the date string formats
    # example: "Mon, 18 Sep 2023 23:13:36 UTC"
    date_pattern1 = r'^[A-Za-z]{3}, \d{2} [A-Za-z]{3} \d{4} \d{2}:\d{2}:\d{2} UTC$'
    # example: "2023-09-18T23:13:36+00:00"
    date_pattern2 = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[\+\-]\d{2}:\d{2}$'
    # example: "2023-09-18 23:13:36.186029+00"
    date_pattern3 = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}[\+\-]\d{2}$'

    class DateParseException(Exception):
        """Custom exception for date parsing errors"""
        pass

    @staticmethod
    def parse_date(date_str):
        parsed_date = None

        # Check if the date string matches the first pattern
        if re.match(DateUtils.date_pattern1, date_str):
            try:
                # If it matches, parse the date string with the first format
                parsed_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
            except ValueError as e:
                raise DateUtils.DateParseException(f"Error parsing date with format '%a, %d %b %Y %H:%M:%S %Z': {e}")

        # Check if the date string matches the second pattern
        elif re.match(DateUtils.date_pattern2, date_str):
            try:
                # If it matches, parse the date string with the second format
                parsed_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError as e:
                raise DateUtils.DateParseException(f"Error parsing date with format '%Y-%m-%dT%H:%M:%S%z': {e}")
        
        # Check if the date string matches the third pattern
        elif re.match(DateUtils.date_pattern3, date_str):
            try:
                # If it matches, parse the date string with the third format
                parsed_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f%z')
            except ValueError as e:
                raise DateUtils.DateParseException(f"Error parsing date with format '%Y-%m-%d %H:%M:%S.%f%z': {e}")

        # If no match for the predefined patterns, try to parse with datetime.fromisoformat
        else:
            try:
                parsed_date = datetime.fromisoformat(date_str)
            except ValueError as e:
                raise DateUtils.DateParseException(f"Error parsing date with datetime.fromisoformat: {e}")

        if parsed_date is None:
            raise DateUtils.DateParseException(f"Unable to parse date: {date_str}")

        return parsed_date

    @staticmethod
    def parse_date_string(date_str, output_date_format):
        parsed_date = DateUtils.parse_date(date_str)
        return parsed_date.strftime(output_date_format)
