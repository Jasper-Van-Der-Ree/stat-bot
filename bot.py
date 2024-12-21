# Stat Bot Code
from datetime import datetime, date, time
import os
import pytz

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False

bot = commands.Bot(intents=intents, command_prefix='/')


@bot.event
async def on_ready():
    """Runs when bot.run is run"""
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    with open('err.log', 'a') as f:
        f.write(f'Unhandled error: {error} | Caused by: {ctx.message}\n')


@bot.command(name='messagecount', description='Counts how many messages were sent in the current channel today')
async def message_count(ctx):
    #Getting our starting point to search the channel history
    timezone = pytz.timezone('EST')
    today = date.today()
    midnight = datetime.combine(today, time())
    start_of_day = timezone.localize(midnight)
    #Getting our history and flattening it into a list
    today_history = ctx.channel.history(after=start_of_day)
    messages = [message async for message in today_history]
    #Letting our user know how many messages have been sent today
    await ctx.send(f"A total of {len(messages)} messages have been sent today")


bot.run(TOKEN)
