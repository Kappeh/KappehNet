from src.command_leaf import Command_Leaf
from src.command_branch import Command_Branch

import src.utils as utils
import random

COMMANDS = Command_Branch("KappehNet v1.0")

# Ping - replies with pong
async def ping(client, user_command, message):
    await client.send_message(message.channel, ':ping_pong: Pong!! xSSS')
COMMANDS.add_command('ping', Command_Leaf(ping, 'Replies with pong.'))

# Dice - rolls a dice
async def dice(client, user_command, message):
    # e.g. '4d20+2,2d10+8d4'
    parameter = ''.join(user_command.split(' ')[1:])
    # e.g. ['4d20+2','2d10+8d4']
    roll_list = parameter.split(',')
    output_string = ''

    for i in range(len(roll_list)):
        dice_list = roll_list[i].split('+')
        running_sum = 0
        roll_values = []

        for dice in dice_list:
            if dice.find('d') == -1:
                if not utils.RepresentsInt(dice):
                    return 'Error parsing dice string.'
                running_sum += int(dice)
                roll_values.append(dice)
            else:
                parts = dice.split('d')
                if len(parts) != 2 or not utils.RepresentsInt(parts[0]) or not utils.RepresentsInt(parts[1]):
                    return 'Error parsing dice string.'
                dice_values = []
                for _ in range(int(parts[0])):
                    value = random.randint(1, int(parts[1]))
                    running_sum += value
                    dice_values.append(str(value))
                roll_values.append('{}({})'.format(dice, ', '.join(dice_values)))
                    
        output_string += 'Roll {}: {} = {}.'.format(i + 1, ' + '.join(roll_values), running_sum)
        if i < len(roll_list) - 1:
            output_string += '\n'

    await client.send_message(message.channel, '```' + output_string + '```')

COMMANDS.add_command('dice', Command_Leaf(dice, 'Rolls a dice.'))