from src.command_leaf import Command_Leaf
from src.command_branch import Command_Branch
from src.command import Param
from PIL import Image
from io import BytesIO
from src.permissions import *

import src.utils as utils
import random
import requests
import discord
import os

from src.quote.quote_manager import QuoteManager

# Main Command Branch --------------------------------------------------------------------------------------------
BOT_NAME = 'KappehNet'
BOT_VERSION = '1.0'
SOURCE_CODE_URL = 'https://github.com/Kappeh/KappehNet'

COMMANDS = Command_Branch(BOT_NAME + ' v' + BOT_VERSION)

# Ping -----------------------------------------------------------------------------------------------------------
async def ping(client, user_command, message):
    await client.send_message(message.channel, ':ping_pong: Pong!! xSSS')

COMMANDS.add_command('ping', Command_Leaf(ping, 'Replies with pong.'))

# Say ------------------------------------------------------------------------------------------------------------
async def say(client, user_command, message):
    em = discord.Embed(title = 'OI.', description = '_*OI.*_', colour = 0x43B581)
    await client.send_message(message.channel, embed = em)

say_params = [
    Param('message', 'The message you want the bot to say.', dtype = 'text', optional = True)
]

COMMANDS.add_command('say', Command_Leaf(say, 'Says your message back to you. ;)', params = say_params))

# Invite Link ----------------------------------------------------------------------------------------------------
async def invite_link(client, user_command, message):
    await client.send_message(message.channel, 'https://discordapp.com/oauth2/authorize?client_id=' + str(client.user.id) + '&scope=bot&permissions=8')

COMMANDS.add_command('invite_link', Command_Leaf(invite_link, 'Invite me to your other servers!'))

# Source code ----------------------------------------------------------------------------------------------------
async def source_code(client, user_command, message):
    await client.send_message(message.channel, 'Source code can be found at: {}.'.format(SOURCE_CODE_URL))

COMMANDS.add_command('source_code', Command_Leaf(source_code, 'Link to {}\'s source code.'.format(BOT_NAME)))

# Info -----------------------------------------------------------------------------------------------------------
async def info(client, user_command, message):
    user = user_command.split(' ')[1]
    chars = '!<@>'
    for c in chars:
        user = user.replace(c, '')
    user = message.server.get_member(user)
    if not user:
        return utils.error_embed('Error.', 'User not found.')

    title = "{}'s Info".format(user.display_name)
    if user.bot == True:
        title += " :robot:"
    em = discord.Embed(title = title, description = "Here's what I could find.", colour = user.colour)
    em.add_field(name = "Name", value = user.name, inline = True)
    if user.nick:
        em.add_field(name = "Nickname", value = user.nick, inline = True)
    em.add_field(name = "ID", value = user.id, inline = True)
    em.add_field(name = "Status", value = user.status, inline = True)
    em.add_field(name = "Highest Role", value = user.top_role, inline = True)
    em.add_field(name = "Joined At", value = user.joined_at, inline = True)
    if user.avatar_url:
        em.set_thumbnail(url = user.avatar_url)

    await client.send_message(message.channel, embed = em)

info_params = [
    Param('user', 'The user you want information about.', dtype = 'mention')
]

COMMANDS.add_command('info', Command_Leaf(info, 'Finds information about a member of this server.', params = info_params))

# Dice -----------------------------------------------------------------------------------------------------------
MAX_DICE_ROLLS = 50
MAX_DICE_FACES = 1000

def get_dice_rolls(dice_string):
    if dice_string.find('d') == -1:
        if not utils.represents_int(dice_string):
            return None, 'Bad dice string.'
        return dice_string, int(dice_string)
    parts = dice_string.split('d')
    if len(parts) != 2 or not utils.represents_int(parts[0]) or not utils.represents_int(parts[1]):
        return None, 'Bad dice string.'
    if int(parts[0]) > MAX_DICE_ROLLS or int(parts[1]) > MAX_DICE_FACES:
        return None, 'Exceeded max limit of {}d{}.'.format(MAX_DICE_ROLLS, MAX_DICE_FACES)
    dice_values = [random.randint(1, int(parts[1])) for _ in range(int(parts[0]))]
    return '{}({})'.format(dice_string, ', '.join([str(i) for i in dice_values])), sum(dice_values)

def get_roll(roll_string):
    dice_list = roll_string.split('+')
    output_strings = []
    output_totals = []
    for dice in dice_list:
        s, t = get_dice_rolls(dice)
        if not s:
            return None, t
        output_strings.append(s)
        output_totals.append(t)
    return ' + '.join(output_strings), sum(output_totals)

async def dice(client, user_command, message):
    raw_string = ''.join(user_command.split(' ')[1:])
    roll_list = raw_string.split(',')
    output_strings = []
    for i in range(len(roll_list)):
        s, t = get_roll(roll_list[i])
        if not s:
            return utils.error_embed('Error while parsing command.', t)
        output_strings.append('Roll {}: {} = {}'.format(i + 1, s, t))
    output_string = '\n'.join(output_strings)
    await client.send_message(message.channel, '```' + output_string + '```')

dice_params = [
    Param('dice_string', 'The ndm command which you want executing.', dtype = 'text', min_len = 3)
]

COMMANDS.add_command('dice', Command_Leaf(dice, 'Rolls dice for you.', params = dice_params))


# Pixelfy --------------------------------------------------------------------------------------------------------
async def pixelfy(client, user_command, message):
    user = user_command.split(' ')[1]
    chars = '!<@>'
    for c in chars:
        user = user.replace(c, '')
    user = message.server.get_member(user)
    if not user:
        return utils.error_embed('Error.', 'User not found.')
    if not user.avatar_url:
        return utils.error_embed('Error.', 'User avatar not found.')
    response = requests.get(user.avatar_url)
    img = Image.open(BytesIO(response.content))

    pixel_size = int(user_command.split(' ')[2])
    img = img.resize((img.size[0] // pixel_size, img.size[1] // pixel_size), Image.NEAREST)
    img = img.resize((img.size[0] * pixel_size, img.size[1] * pixel_size), Image.NEAREST)

    img.save('tmp.png')
    await client.send_file(message.channel, 'tmp.png', filename = 'pixelated.png')
    os.remove('tmp.png')

pixelfy_params = [
    Param('user', 'The user that you wish to pixelfy.', dtype = 'mention'),
    Param('pixel_size', 'The amount that you want to pixelfy.', dtype = 'int', min_val = 2, max_val = 30)
]

COMMANDS.add_command('pixelfy', Command_Leaf(pixelfy, 'Pixelates your friends.', params = pixelfy_params))

# Quote ----------------------------------------------------------------------------------------------------------
QUOTE_ERRORS = ['Sorry bud. I can\'t help you. ', 
                'I don\'t know any good quotes. Maybe you can tell me one!',
                'I would if I would, but I cant.',
                'A dog once wondered across the street.',
                'I\'m out of ideas.',
                'Sorry!',
                'Last one, I promise!']
QUOTE_TITLES = ['I went through blood, sweat, and tears whilst reading {0}',
                'Have you seen {0}? Spoiler alert!',
                'I\'ve dedicated this quote to you, {1}. It\'s from {0}',
                'Hehe... it\'s from {0}']

NUM_QUOTE_ERRORS = len(QUOTE_ERRORS)
NUM_QUOTE_TITLES = len(QUOTE_TITLES)

QUOTES_FILE_PATH = 'res/quotes.txt'

quotemanager = QuoteManager(QUOTES_FILE_PATH)

async def quote_func(client, user_command, message):
    if not quotemanager.loaded:
        quotemanager.load()

    quote = quotemanager.pickRandomQuote()
    if not quote:
        errorIndex = random.randint(0, NUM_QUOTE_ERRORS - 1)
        return utils.error_embed('Oops.', QUOTE_ERRORS[errorIndex])

    text = quote.text
    origin = quote.origin

    titleIndex = random.randint(0, NUM_QUOTE_TITLES - 1)
    title = QUOTE_TITLES[titleIndex].format(origin, message.author.display_name)
    
    em = discord.Embed(title = title, colour = 0x43B581, description = text)
    await client.send_message(message.channel, embed = em)

COMMANDS.add_command('quote', Command_Leaf(quote_func, 'Fetches a funny quote. Like a dog.'))

# Help -----------------------------------------------------------------------------------------------------------
async def help_func(client, user_command, message):
    argv = user_command.split(' ')[1:]
    help_message = COMMANDS.get_help_message(*argv)
    if isinstance(help_message, discord.Embed):
        return help_message
    help_message += '\nUse `@{} help <command>` to get more information.\n'.format(client.user.name)
    em = discord.Embed(title = 'Help', description = help_message, colour = 0x43B581)
    await client.send_message(message.channel, embed = em)

help_func_params = [
    Param('cmd', 'The command which you need help with.', dtype = 'text', optional = True)
]

COMMANDS.add_command('help', Command_Leaf(help_func, 'Shows help messages.', params = help_func_params))
