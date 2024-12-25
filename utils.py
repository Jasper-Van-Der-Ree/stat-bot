"""Generic function storage"""

import datetime
import json

from discord import TextChannel
from pytoolz import get_in


def cache_count(date: datetime, channel: TextChannel, user_id: int, count: int):
    """Caches the amount of messages sent by a user on a given day in a given channel
    Args:
        date: date messages were sent on
        channel: channel messages were sent in
        user_id: user messages were sent by
        count: amount of messages on date in channel by user
    """
    with open('cache.json', 'w') as f:
        cache = json.load(f)
        channel_id = channel.id
        date_key = date.strftime('%Y-%m-%d')
        cache[channel_id][date_key][user_id] = count            
        json.dump(cache, f)


def retrieve_count(date: datetime, channel: TextChannel, user_id: int):
    """Retrieves the amount of messages sent by a user on a given day in a given channel
    Args:
        date: date messages were sent on
        channel: channel messages were sent in
        user_id: user messages were sent by
    """
    with open('cache.json', 'r') as f:
        cache = json.load(f)
        channel_id = channel.id
        date_key = date.strftime('%Y-%m-%d')
        return get_in(keys=[channel_id, date_key, user_id], coll=cache, default=None)
