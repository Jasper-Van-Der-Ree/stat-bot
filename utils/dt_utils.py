"""Datetime Function Storage"""

from datetime import date, datetime, time, timedelta
import pytz


def todays_date(timezone: str = 'EST') -> str:
    tz = pytz.timezone(timezone)
    now = datetime.now()
    return tz.localize(now).strftime('%Y-%m-%d')


def get_today() -> tuple[datetime]:
    """Gets the start of today and current time"""
    timezone = pytz.timezone('EST')
    today = date.today()
    today_midnight = datetime.combine(today, time())
    now = datetime.now()
    return timezone.localize(today_midnight), timezone.localize(now)


def get_yesterday() -> tuple[datetime]:
    """Gets the start of yesterday and current time"""
    timezone = pytz.timezone('EST')
    today = date.today()
    today_midnight = datetime.combine(today, time())
    yesterday_midnight = today_midnight - timedelta(days=1)
    return timezone.localize(yesterday_midnight), timezone.localize(today_midnight)


def get_this_week() -> tuple[datetime]:
    """Gets the start of the calendar week and current time"""
    timezone = pytz.timezone('EST')
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week_midnight = datetime.combine(start_of_week, time())
    now = datetime.now()
    return timezone.localize(start_of_week_midnight), timezone.localize(now)


def get_this_month() -> tuple[datetime]:
    """Gets the start of the calendar month and current time"""
    timezone = pytz.timezone('EST')
    today = date.today()
    start_of_month = today.replace(day=1)
    start_of_month_midnight = datetime.combine(start_of_month, time())
    now = datetime.now()
    return timezone.localize(start_of_month_midnight), timezone.localize(now)
