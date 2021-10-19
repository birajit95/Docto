from dateutil.relativedelta import relativedelta
from datetime import datetime


def calculate_age(date_of_birth):
    delta = relativedelta(datetime.now(), date_of_birth)
    return {
        "year": delta.years,
        "month": delta.months,
        "day": delta.days
    }