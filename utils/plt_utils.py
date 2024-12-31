"""Data Visualization Function Storage"""

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from toolz.dicttoolz import get_in

days_of_the_week = ['S', 'S', 'M', 'T', 'W', 'T', 'F']


def graph_activity(
    start: datetime,
    end: datetime,
    channel_hist: dict,
    user_id: str,
    filename: str,
    channel_name: str,
    period: str, 
    user_name: str = None,
) -> None:
    """Graphs user activity on a histogram for a period of time

    Args:
        start: start of the period to graph
        end: end of the period to graph
        channel_hist: dictionary with all date counts
        user_id: ID of the user we're plotting 
        filename: name of the file we're saving
        channel_name: name of the channel
        period: period we're generating a graph for
        user_name: name of the user
    """
    timespan = end - start
    history = {}
    # xticks = []
    for i in range(timespan.days): # Finding all of our relevant values and adding them to history 
        day = start + timedelta(days=i)
        day_key = day.strftime('%Y-%m-%d')
        # xticks += days_of_the_week[day.weekday()]
        history[day_key] = get_in([day_key, user_id], channel_hist)
    
    fig, ax = plt.subplots()
    fig = ax.figure
    fig.autofmt_xdate(rotation=270, ha='center')
    xticks = [x[5:] for x in history.keys()]
    ax.bar(xticks, history.values())
    if user_name:
        ax.set_title(f"Messages sent in {channel_name} by {user_name} {period}")
    else:
        ax.set_title(f"Messages sent in {channel_name} {period}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Messages sent")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    fig.savefig(filename, bbox_inches='tight')
