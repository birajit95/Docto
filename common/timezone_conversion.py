from pytz import timezone


def convert_tz(dt_object, user_timezone='Asia/Kolkata'):
    TIME_ZONE_TIME_FORMAT = '%H:%M:%S'
    TIME_ZONE_DATE_FORMAT = '%Y-%m-%d'
    TIME_ZONE_DATETIME_FORMAT = f"{TIME_ZONE_DATE_FORMAT}::{TIME_ZONE_TIME_FORMAT}"
    user_tz = timezone(user_timezone)
    user_datetime = dt_object.astimezone(user_tz)
    user_datetime = user_tz.normalize(user_datetime).strftime(TIME_ZONE_DATETIME_FORMAT)
    return user_datetime
