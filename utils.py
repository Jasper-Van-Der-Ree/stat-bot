from datetime import date, datetime, time, timedelta
from discord import HTTPException
import pytz
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


def get_today() -> tuple[datetime]:
    """Gets the start of today and current time"""
    timezone = pytz.timezone('EST')
    today = date.today()
    today_midnight = datetime.combine(today, time())
    now = datetime.now()
    return timezone.localize(today_midnight), timezone.localize(now)


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


@retry(
    reraise=True,
    retry=retry_if_exception_type(HTTPException),
    wait=wait_exponential(multiplier=1, min=5, max=10),
)
def get_channel_history(interaction, after, before):
    """Get channel history for some window of time"""
    return interaction.channel.history(after=after, before=before, limit=None)

