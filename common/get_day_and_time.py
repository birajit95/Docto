from datetime import datetime


def get_day():
    now = datetime.now()
    day = str(now.strftime("%A").upper())
    return day


def get_time():
    now = datetime.now()
    time = str(now.strftime("%H:%M"))
    return time


