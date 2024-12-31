"""Stat Bot Code"""

from asyncio import run
from os import getenv, remove
from typing import Literal

import discord
from discord import app_commands, Activity, Interaction, File, Object, Member
from discord.ext import commands
from dotenv import load_dotenv

from utils.api_utils import chunk_get_history
from utils.cache_utils import get_cache, save_cache
from utils.dt_utils import get_today, get_yesterday, get_this_week, get_this_month, todays_date
from utils.gen_utils import count_user_channel_messages, count_channel_messages
from utils.plt_utils import graph_activity

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
GUILD_ID = getenv('DISCORD_GUILD_ID')

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
bot = commands.Bot(intents=intents, command_prefix='/')


@bot.event
async def setup_hook() -> None:
    await bot.tree.sync(guild=Object(GUILD_ID))


@bot.event
async def on_ready() -> None:
    """Runs when the bot starts up"""
    activity = Activity(type=discord.ActivityType.watching, name="chat")
    await bot.change_presence(activity=activity)
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_app_command_error(interaction: Interaction, error: app_commands.AppCommandError) -> None:
    """Runs when a command triggers an exception"""
    if interaction.message:
        async with open('err.log', 'a') as f:
            f.write(f'Unhandled error: {error} | Caused by: {interaction.message.content}\n')
    else:
        async with open('err.log', 'a') as f:
            f.write(f'Unhandled error: {error} | Command: {interaction.command} | User: {interaction.user} | Channel: {interaction.channel}\n')

    if isinstance(error, app_commands.errors.CommandOnCooldown):
        if not interaction.response.is_done():
            await interaction.response.send_message(
                f'command "{interaction.command.name}" is on cooldown. you can use it in {round(error.retry_after, 2)} seconds.',
                ephemeral=True  
            )
        else:
            await interaction.followup.send(
                f'command "{interaction.command.name}" is on cooldown, you can use it in {round(error.retry_after, 2)} seconds.',
                ephemeral=True
            )
    else: 

        if not interaction.response.is_done():
            await interaction.response.send_message("an unexpected error occurred. please try again later.", ephemeral=True)
        else:
            await interaction.followup.send("an unexpected error occurred. please try again later.", ephemeral=True)


@bot.tree.command(
        name = 'messagecount',
        description = 'Counts how many messages were sent in a given period by a given',
        guild = Object(id=GUILD_ID)
)
async def message_count(
    interaction: Interaction,
    period: Literal["today", "yesterday", "this week", "this month"],
    member: Member = None,
    graph: bool = False,
) -> None:
    await interaction.response.defer()
    # Handling period options
    if period == 'today':
        start, end = get_today()
        verb = "have been"
    elif period == 'yesterday':
        start, end = get_yesterday()
        verb = "were"
    elif period == 'this week':
        start, end = get_this_week()
        verb = "have been"
    elif period == 'this month':
        start, end = get_this_month()
        verb = "have been"
    else:
        await interaction.followup.send("Please provide a valid period", ephemeral=True)
        raise InvalidArgument

    # Gets a dictionary containing date:history pairs, where history is an async iterable of messages
    history = chunk_get_history(channel=interaction.channel, after=start, before=end)
    # Gets our count cache
    cache = get_cache('resources/cache.json')
    # Gets today's date in EST
    today = todays_date('EST')
    # Gets our channel ID and user ID
    channel_id = str(interaction.channel.id)
    if member: # Are we looking for messages from a particular user?
        user_id = str(member.id)
        count = await count_user_channel_messages(history, cache, today, channel_id, user_id)
        user_name = member.nick if member.nick else member.global_name
        await interaction.followup.send(f"{count} messages {verb} sent by {user_name} {period}")
    else: # Count messages from all users instead
        user_id = "0"
        count = await count_channel_messages(history, cache, today, channel_id)
        user_name = None
        await interaction.followup.send(f"{count} messages {verb} sent {period}")

    save_cache(cache)
    if graph and period != "today": # Are we looking to display a histograph showing messages per day?
        filename='resources/temp.png'
        channel_name = interaction.channel.name
        graph_activity(start, end, cache[channel_id], user_id, filename, channel_name, period, user_name)
        await interaction.followup.send(file=File(filename))
        remove(filename)


async def main():
    await bot.start(TOKEN)

run(main())
