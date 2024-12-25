"""API Function Storage"""

from datetime import datetime, timedelta, time

from discord import HTTPException, TextChannel
from tenacity import (
    retry,
    retry_if_exception_type,
    wait_exponential,
)


@retry(
    reraise=True,
    retry=retry_if_exception_type(HTTPException),
    wait=wait_exponential(multiplier=1, min=5, max=10),
)
def get_channel_history(channel: TextChannel, after: datetime, before: datetime):
    """Gets channel history for some window of time
    Args:
        channel: channel where the slash command was run
        after: after of the period we want messages from
        before: before of the period we want messages from
    Returns:
        An asynchronous iterator with relevant channel history
    """
    return channel.history(after=after, before=before, limit=5000)


def chunk_get_history(channel: TextChannel, after: datetime, before: datetime) -> dict:
    """Chunks get_channel_history into day-sized chunks so that we don't timeout discord API
    Args:
        channel: channel where the slash command was run
        after: after of the period we want messages from
        before: before of the period we want messages from
    Returns:
        An asynchronous iterator with the relevant channel history
    """
    timespan = before - after
    history = {}
    for i in range(timespan.days):
        after_day = after + timedelta(days=i)
        before_day = after_day + timedelta(days=1)
        date = after_day.strftime('%Y-%m-%d')
        history[date] = get_channel_history(channel=channel, after=after_day, before=before_day)

    last_midnight = datetime.combine(before, time())
    last_date = before.strftime('%Y-%m-%d')
    history[last_date] = get_channel_history(channel=channel, after=last_midnight, before=before)
    return history
