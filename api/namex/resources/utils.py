from dateutil import parser


class DateUtils:

    @staticmethod
    def parse_date(date_str):
        return parser.parse(date_str)

    @staticmethod
    def parse_date_string(date_str, output_date_format):
        parsed_date = parser.parse(date_str)
        return parsed_date.strftime(output_date_format)
