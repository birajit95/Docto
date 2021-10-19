from datetime import datetime


def _12hours_to_24hours(time):
    _12hours = datetime.strptime(str(time), "%I:%M %p")
    _24hours = datetime.strftime(_12hours, "%H:%M")
    return _24hours


def _24hours_to_12hours(time):
    _24hours = datetime.strptime(str(time), "%H:%M:00")
    _12hours = datetime.strftime(_24hours, "%I:%M %p")
    return _12hours
