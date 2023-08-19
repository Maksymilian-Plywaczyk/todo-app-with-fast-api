from datetime import datetime, timedelta
from time import mktime
from typing import Union

import parsedatetime


def convert_human_read_date_to_datetime(date_string: str) -> Union[datetime, None]:
    """Convert human readable date to datetime object."""
    now = datetime.now()
    if date_string == "":
        return datetime.today()
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(date_string)
    if parse_status != 0:
        parsed_datetime = datetime(*time_struct[:6])
        if parsed_datetime < now:
            return parsed_datetime + timedelta(days=1)
        return datetime.fromtimestamp(mktime(time_struct))
    return None
