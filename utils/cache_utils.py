"""Cache Function Storage"""

import json


def get_cache(filename: str) -> dict:
    """Reads and returns the cache"""
    with open(filename, 'r') as f:
        cache = json.load(f)
        return cache


def update_cache(cache: dict, channel_id: str, day: str, user_id: str, day_count: int) -> dict:
    """Takes the loaded cache and injects the given channel, day, user combination

    Args:
        cache: the loaded cache
        channel_id: ID of the channel messages were sent in
        day: the day messages were sent on
        user_id: the user that sent the messages
        day_count: the amount of messages sent

    Returns:
        cache with the injected value
    """
    channel_dct = cache.get(channel_id)
    if channel_dct: # If the channel key exists in cache
        day_dct = channel_dct.get(day)
        if day_dct: # If the day key exists in channel dict
            cache[channel_id][day][user_id] = day_count
        else: # If no day key in channel dict
            cache[channel_id][day] = {user_id: day_count}
    else: # If no channel key in cache
        cache[channel_id] = {day: {user_id: day_count}}


def save_cache(cache: dict) -> None:
    """Takes the cache and saves it locally"""
    with open('resources/cache.json', 'w') as f:
        json.dump(cache, f, indent=4)
