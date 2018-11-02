from src.command_node import Command_Node
from src.command_branch import Command_Branch

COMMANDS = Command_Branch("KappehNet v1.0")

async def ping(client, user_command, message):
    await client.send_message(message.channel, ':ping_pong: Pong!! xSSS')
COMMANDS.add_command('ping', Command_Node(ping, 'Replies with pong.'))