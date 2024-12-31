"""Data Visualization Function Storage"""

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from toolz.dicttoolz import get_in


def graph_activity(start: datetime, end: datetime, channel_hist: dict, user_id: str) -> None:
    """Graphs user activity on a histogram for a period of time

    Args:
        start: start of the period to graph
        end: end of the period to graph
        channel_hist: dictionary with all date counts
        user_id: ID of the user we're plotting 
    """
    timespan = end - start
    history = {}
    for i in range(timespan.days): # Finding all of our relevant values and adding them to history 
        day = start + timedelta(days=i)
        day_key = day.strftime('%Y-%m-%d')
        history[day_key] = get_in([day_key, user_id], channel_hist)
    
    fig, ax = plt.subplots()
    ax.bar(history.keys(), history.values(), color='w')
    ax.set_xticks(rotation=45)
    fig.savefig('resources/temp.png', bbox_inches='tight', facecolor='white')
