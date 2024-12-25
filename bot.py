"""Stat Bot Code"""

import asyncio
import os
from typing import Literal

import discord
from discord import app_commands, Interaction
from discord.ext import commands
from dotenv import load_dotenv

from api_utils import chunk_get_history
from dt_utils import get_today, get_this_week, get_this_month

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
bot = commands.Bot(intents=intents, command_prefix='/')


@bot.event
async def setup_hook():
    await bot.tree.sync(guild=discord.Object(GUILD_ID))


@bot.event
async def on_ready():
    """Runs when the bot starts up"""
    activity = discord.Activity(type=discord.ActivityType.watching, name="chat")
    await bot.change_presence(activity=activity)
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    """Runs when a command triggers an unhandled exception"""
    with open('err.log', 'a') as f:
        f.write(f'Unhandled error: {error} | Caused by: {ctx.message}\n')


@bot.tree.command(
        name = 'messagecount',
        description = 'Counts how many messages were sent in a given period by a given',
        guild = discord.Object(id=GUILD_ID)
)
async def message_count(interaction: Interaction, period: Literal["today", "this week", "this month"], member: discord.Member = None):
    await interaction.response.defer()
    #Getting our period start
    if period == 'today':
        start, end = get_today()
    elif period == 'this week':
        start, end = get_this_week()
    elif period == 'this month':
        start, end = get_this_month()
    else:
        await interaction.followup.send("Please provide a valid period", ephemeral=True)
        raise discord.InvalidArgument

    combined_stream = chunk_get_history(interaction, start, end)
    async with combined_stream.stream() as history:
        if member:
            length = len([message async for message in history if message.author.id == member.id])
            name = member.nick if member.nick else member.global_name
            await interaction.followup.send(f"{length} messages have been sent here {period} by {name}")
        else:
            length = len([message async for message in history])
            await interaction.followup.send(f"{length} messages have been sent here {period}")
    
    del combined_stream


async def main():
    await bot.start(TOKEN)

asyncio.run(main())
