# Stat Bot Code
import asyncio
import os
from typing import Literal

import discord
from discord import app_commands, Interaction
from discord.ext import commands
from dotenv import load_dotenv

from utils import get_today_start, get_week_start


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
    activity = discord.Activity(type=discord.ActivityType.watching, name="Chat")
    await bot.change_presence(activity=activity)
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    """Runs when a command triggers an unhandled exception"""
    with open('err.log', 'a') as f:
        f.write(f'Unhandled error: {error} | Caused by: {ctx.message}\n')


@bot.tree.command(
        name = 'messagecount',
        description = 'Counts how many messages were sent in a given period',
        guild = discord.Object(id=GUILD_ID)
)
async def today_message_count(interaction: Interaction, period: Literal["Today", "This Week"]):
    #Getting our period start
    if period == 'Today':
        start = get_today_start()
    elif period == 'This Week':
        start = get_week_start()
    else:
        await interaction.response.send_message("Please provide a valid period", ephemeral=True)
        raise discord.InvalidArgument
    #Getting our message history
    history = interaction.channel.history(after=start)
    messages = [message async for message in history]
    #Broadcasting how many messages have been sent
    await interaction.response.send_message(f"{len(messages)} messages have been sent since the start of {start.strftime('%a %d %b %Y')}")


async def main ():
    await bot.start(TOKEN)

asyncio.run(main())
