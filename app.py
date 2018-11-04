# KappehNet version 1.0 Alpha
# Made by Kappeh
# https://github.com/Kappeh/KappehNet

import os
import sys
import discord
import configparser
import src.utils as utils
from config import OWNER
from src.commands import COMMANDS

TOKEN = os.environ.get('DISCORD_TOKEN')
if not TOKEN:
    if os.path.isfile('auth.ini'):
        config = configparser.ConfigParser()
        config.read('auth.ini')
        TOKEN = config.get('discord', 'token')
    elif len(sys.argv) > 1:
        TOKEN = sys.argv[1]
    else:
        raise Exception('Specify discord token either with a auth.ini file or as an argument.')

CLIENT = discord.Client()
LOG_USER = {'name': OWNER}

def log(msg, first_log = False):
    timestamp_msg = utils.get_time() + msg
    print(timestamp_msg)
    if first_log:
        timestamp_msg = '-' * 90 + '\n' + timestamp_msg
    if 'member' in LOG_USER:
        return CLIENT.send_message(LOG_USER['member'], timestamp_msg)

@CLIENT.event
async def on_ready():
    for member in CLIENT.get_all_members():
        if str(member) == LOG_USER['name']:
            LOG_USER['member'] = member
    await log('Bot logged in with name: {} and id: {}.'.format(CLIENT.user.name, CLIENT.user.id), first_log = True)

@CLIENT.event
async def on_message(message):
    prefix = '<@' + CLIENT.user.id + '> '
    user_command = ''
    if message.content.startswith(prefix):
        user_command = message.content.replace(prefix, '', 1)
    elif not message.server:
        user_command = message.content

    if CLIENT.user.id != message.author.id and user_command:
        log_message = str(message.author) + ' ran: "' + user_command + '"'
        if message.server:
            log_message += ' in server: {}.'.format(message.server.name)
        else:
            log_message += ' in a private message.'
        log_routine = log(log_message)
        if LOG_USER['name'] != str(message.author) or message.server:
            await log_routine

        output = await COMMANDS.execute(user_command, CLIENT, user_command, message)
        if isinstance(output, str):
            await CLIENT.send_message(message.channel, output)

CLIENT.run(TOKEN)