from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta 
from rest_framework.response import Response

def time_checker(updated_at, hour=None, minute=None):
    current_time = datetime.now().time()
    updated_time = updated_at.time()

    current_timedelta = timedelta(hours=current_time.hour, minutes=current_time.minute,
                                           seconds=current_time.second)
    updated_timedelta = timedelta(hours=updated_time.hour, minutes=updated_time.minute,
                                           seconds=updated_time.second)
    time_difference = current_timedelta - updated_timedelta

    given_time = None
    if hour:
        given_time = timedelta(hours=hour)
    elif minute:
        given_time = timedelta(minutes=minute)

    return time_difference > given_time if given_time else False


def time_frame_validator(time):
    # amount, unit = int(timeframe[:-5]), timeframe[-5:]
    value = ''
    unit = ''
    
    for char in time:
        if char.isdigit():
            value += char
        else:
            unit += char
    
    if not value.isdigit() or unit == '':
        return Response("Invalid duration format", 400)  
    
    value = int(value)
    current_time = datetime.now()
    unit = unit.lower()

    unit_map = {
        'day': timedelta(days=value),
        'days': timedelta(days=value),
        'week': timedelta(weeks=value),
        'weeks': timedelta(weeks=value),
        'month': relativedelta(months=value),
        'months': relativedelta(months=value),
        'year': relativedelta(years=value),
        'years': relativedelta(years=value)
    }

    if unit in unit_map:
        query_date = current_time - unit_map[unit]
        return query_date
    else:
        return Response("Invalid time unit", status=400)
