from inspect import iscoroutinefunction
from src.command import Command
from src.command_node import Command_Node

class Command_Branch(Command):

    def __init__(self, brief, function = None, description = None, **kwargs):
        self._brief = brief
        self._description = description
        self._meta = kwargs

        self._function = function
        self._commands = {}
    
    def get_command(self, cmd, *argv):
        if not isinstance(cmd, str):
            return None
        cmd = cmd.lower()

        if cmd in self._commands:
            if len(argv) != 0 and isinstance(self._commands[cmd], Command_Branch):
                return self._commands[cmd].get_command(*argv)
            return self._commands[cmd]
        
        return None

    def validate_add_command(self, cmd_string, cmd):
        if not isinstance(cmd_string, str):
            raise ValueError('Command name must be a string.')
        if len(cmd_string) == 0:
            raise ValueError('Command name must have at least length 1.')
        if self.get_command(cmd_string) != None:
            raise ValueError('Command already exists.')
        if not (isinstance(cmd, Command_Node) or isinstance(cmd, Command_Branch)):
            raise ValueError('Command must be a Command Node or Command Branch.')

    def add_command(self, cmd_string, cmd):
        self.validate_add_command(cmd_string, cmd)
        cmd_string = cmd_string.lower()

        self._commands[cmd_string] = cmd
    
    async def execute(self, cmd_to_execute, *argv, **kwargs):
        cmd_argv = cmd_to_execute.split(' ')
        cmd = self.get_command(*cmd_argv)

        if cmd == None:
            return 'Error. Unable to find command.'

        if cmd._function and callable(cmd._function):
            if iscoroutinefunction(cmd._function):
                return await cmd._function(*argv, **kwargs)
            else:
                return cmd._function(*argv, **kwargs)
        
        return 'Error. could not find a callable in the command object.'
        
    def get_help_message(self, *argv):
        cmd = self
        result = ''
        if len(argv) != 0:
            cmd = self.get_command(*argv)
            result = ' '.join(argv) + ' - '
        
        if cmd == None:
            return None

        result += cmd.get_help(description = isinstance(cmd, Command_Node))

        if isinstance(cmd, Command_Branch):
            result += '\n\n'
            result += 'Sub Commands:\n'
            for scmd in cmd._commands.keys():
                result += '    {} - {}\n'.format(scmd, cmd._commands[scmd].get_help())

        return result