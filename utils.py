from datetime import date, datetime, time, timedelta
import pytz


def get_today_start():
    """Gets the start of the day"""
    timezone = pytz.timezone('EST')
    today = date.today()
    today_midnight = datetime.combine(today, time())
    return timezone.localize(today_midnight)

def get_week_start():
    """Gets the start of the calendar week"""
    timezone = pytz.timezone('EST')
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week_midnight = datetime.combine(start_of_week, time())
    return timezone.localize(start_of_week_midnight)