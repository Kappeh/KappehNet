from src.command_leaf import Command_Leaf
from src.command_branch import Command_Branch

import src.utils as utils
import random
import discord

# Main Command Branch --------------------------------------------------------------------------------------------
BOT_NAME = 'KappehNet'
BOT_VERSION = '1.0'
SOURCE_CODE_URL = 'https://github.com/Kappeh/KappehNet'

COMMANDS = Command_Branch(BOT_NAME + ' v' + BOT_VERSION)

# Ping -----------------------------------------------------------------------------------------------------------
async def ping(client, user_command, message):
    await client.send_message(message.channel, ':ping_pong: Pong!! xSSS')

COMMANDS.add_command('ping', Command_Leaf(ping, 'Replies with pong.'))

# Source code ----------------------------------------------------------------------------------------------------
async def source_code(client, user_command, message):
    await client.send_message(message.channel, 'Source code can be found at: {}.'.format(SOURCE_CODE_URL))

COMMANDS.add_command('source_code', Command_Leaf(source_code, 'Link to {}\'s source code.'.format(BOT_NAME)))

# Info -----------------------------------------------------------------------------------------------------------
async def info(client, user_command, message):
    user = ''.join(user_command.split(' ')[1:])
    chars = '!<@>'
    for c in chars:
        user = user.replace(c, '')
    if user == '':
        return 'Please enter a user to find information about.'
    user = message.server.get_member(user)
    if not user:
        return 'User not found.'

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

COMMANDS.add_command('info', Command_Leaf(info, 'Finds information about a member of this server.'))

# Dice -----------------------------------------------------------------------------------------------------------
MAX_DICE_ROLLS = 50
MAX_DICE_FACES = 1000

def get_dice_rolls(dice_string):
    if dice_string.find('d') == -1:
        if not utils.RepresentsInt(dice_string):
            return None, 'Error parsing command.'
        return dice_string, int(dice_string)
    parts = dice_string.split('d')
    if len(parts) != 2 or not utils.RepresentsInt(parts[0]) or not utils.RepresentsInt(parts[1]):
        return None, 'Error parsing command.'
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
            return t
        output_strings.append('Roll {}: {} = {}'.format(i + 1, s, t))
    output_string = '\n'.join(output_strings)
    await client.send_message(message.channel, '```' + output_string + '```')

COMMANDS.add_command('dice', Command_Leaf(dice, 'Rolls dice for you.'))

# Help -----------------------------------------------------------------------------------------------------------
async def help_func(client, user_command, message):
    argv = user_command.split(' ')[1:]
    help_message = '```\n' + COMMANDS.get_help_message(*argv) + '\n'
    help_message += 'Use @{} help <command> to get more information.\n```'.format(client.user.name)
    await client.send_message(message.channel, help_message)
COMMANDS.add_command('help', Command_Leaf(help_func, 'Shows help messages.'))