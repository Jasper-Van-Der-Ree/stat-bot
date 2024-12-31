"""General utility functions"""

from datetime import datetime

from toolz.dicttoolz import get_in

from utils.cache_utils import update_cache


async def count_user_channel_messages(
    history: dict, cache: dict,today: datetime, channel_id: str, user_id: str
) -> int:
    """Counts messages sent by a particular user over a given channel history
    Finds previously found message counts for past dates and stores new ones

    Args:
        history: dictionary with date:message iterator pairs
        cache: stores results of previous message counts
        today: current date
        channel_id: ID of the channel where messages were sent
        user_id: ID of user who we're counting the messages of

    Returns:
        Count of messages sent by the provided user in some channel
    """
    count = 0
    for day, messages in history.items():
        # Access our counts cache
        day_count = get_in([channel_id, day, user_id], cache)
        if not day_count: # If we do not have this count cached
            user_id_num = int(user_id)
            day_count = len([None async for message in messages if message.author.id == user_id_num])
            if day != today: # Do not cache today, message history is not yet complete!
                update_cache(cache, channel_id, day, user_id, day_count)

        count += day_count

    return count


async def count_channel_messages(
    history: dict, cache: dict, today: datetime, channel_id: str
) -> int:
    """Counts messages sent by in a channel over a given history
    Finds previously found message counts for past dates and stores new ones

    Args:
        history: dictionary with date:message iterator pairs
        cache: stores results of previous message counts
        today: current date
        channel_id: ID of the channel where messages were sent

    Returns:
        Count of messages sent in a channel
    """
    user_id = "0"
    count = 0
    for day, messages in history.items():
        day_count = get_in([channel_id, day, user_id], cache)
        if not day_count: # If we do not have this count cached
            day_count = len([None async for _ in messages])
            if day != today: # Do not cache today, message history is not yet complete
                update_cache(cache, channel_id, day, user_id, day_count)

        count += day_count

    return count
