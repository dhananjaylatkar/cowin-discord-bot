import os
import discord
from discord.ext import tasks
from cowin import cowin
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w+')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

client = discord.Client()
cowin = cowin()
pincodes = {'Mukhed': '431715', 'Nanded': '431605'}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    test.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name == 'cowin':
        if message.content.startswith('$all'):
            for place, pin in pincodes.items():
                data = cowin.format_data(cowin.get_data(pin), True)
                if data:
                    await message.channel.send('All slot(s) in {}'.format(place))
                    await message.channel.send('```' + data + '```')


@tasks.loop(seconds=10.0)
async def test():
    channel = client.get_channel(843153394213847051)
    for place, pin in pincodes.items():
        data = cowin.format_data(cowin.get_data(pin))
        if data:
            await channel.send('Found Slot(s) in {}'.format(place))
            await channel.send('```' + data + '```')

client.run(os.getenv('COWIN_BOT'))
