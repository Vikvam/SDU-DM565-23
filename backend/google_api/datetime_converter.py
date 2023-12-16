from datetime import datetime, time, timedelta

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
TIME_FORMAT = "%H:%M"


def convert_str_to_datetime(value: str) -> datetime:
    return datetime.strptime(value, DATETIME_FORMAT)


def convert_datetime_to_str(value: datetime) -> str:
    return value.strftime(DATETIME_FORMAT)


def combine_date_with_time(datetime_val: datetime | str, time_val: str) -> datetime:
    if isinstance(datetime_val, str):
        datetime_val = convert_str_to_datetime(datetime_val)

    time_val = convert_str_to_time(time_val)

    if datetime_val.hour > time_val.hour:
        datetime_val += timedelta(days=1)

    return datetime.combine(datetime_val, time_val)


def convert_str_to_time(value: str) -> time:
    return datetime.strptime(value, TIME_FORMAT).time()
