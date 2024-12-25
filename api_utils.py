"""API Function Storage"""

from aiostream import stream
from datetime import datetime, timedelta, time
from discord import HTTPException, Interaction
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
def get_channel_history(interaction: Interaction, after: datetime, before: datetime):
    """Get channel history for some window of time
    Args:
        interaction: Discord interaction, the slash command instance
        after: after of the period we want messages from
        before: before of the period we want messages from
    Returns:
        An asynchronous iterator with relevant channel history
    """
    return interaction.channel.history(after=after, before=before, limit=None)


def chunk_get_history(interaction: Interaction, after: datetime, before: datetime):
    """Chunks get_history into day-sized chunks that we don't timeout discord API
    Args:
        interaction: Discord interaction, the slash command instance
        after: after of the period we want messages from
        before: before of the period we want messages from
    Returns:
        An asynchronous iterator with the relevant channel history
    """
    timespan = before - after
    grand_history = []
    for i in range(timespan.days):
        after_day = after + timedelta(days=i)
        before_day = after_day + timedelta(days=1)
        grand_history.append(
            get_channel_history(interaction=interaction, after=after_day, before=before_day)
        )
    last_midnight = datetime.combine(before, time())
    grand_history.append(
        get_channel_history(interaction=interaction, after=last_midnight, before=before)
    )
    return stream.merge(*grand_history)
