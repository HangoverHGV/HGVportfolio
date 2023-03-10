from datetime import datetime, timedelta
import calendar


def remaining_days(start, end):

    start_datetime = datetime.strptime(start, '%Y-%m-%d %H:%M')
    end_datetime = datetime.strptime(end, '%Y-%m-%d %H:%M')

    delta = end_datetime - start_datetime

    start_month = start_datetime.month
    end_month = end_datetime.month

    start_date = start_datetime.strftime('%Y-%m-%d')
    end_date = end_datetime.strftime('%Y-%m-%d')

    folder_name = f'{start_datetime.day}_{calendar.month_abbr[start_datetime.month]}-{end_datetime.day}_{calendar.month_abbr[end_datetime.month]}'
    month_name = calendar.month_abbr[start_datetime.month]
    out = {
        'delta_days': delta.days,
        'folder_name': folder_name,
        'start_date': start_date,
        'end_date': end_date,
        'start_month': start_month,
        'end_month': end_month,
        'month_name': month_name
    }

    return out

def days_between(start, end, desired_month):
    start_datetime = datetime.strptime(start, '%Y-%m-%d %H:%M')
    end_datetime = datetime.strptime(end, '%Y-%m-%d %H:%M')

    date_list = []
    date = start_datetime
    while date <= end_datetime:
        if date.month == desired_month:
            date_list.append(date.strftime('%Y-%m-%d'))
        date += timedelta(days=1)

    return date_list

def hours_stayed(start, end):
    start_datetime = datetime.strptime(start, '%Y-%m-%d %H:%M')
    end_datetime = datetime.strptime(end, '%Y-%m-%d %H:%M')

    hours = (end_datetime - start_datetime).total_seconds() / 3600

    return hours

