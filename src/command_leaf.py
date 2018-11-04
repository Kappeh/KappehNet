from inspect import iscoroutinefunction
from src.command import Command
import src.utils as utils

class Command_Leaf(Command):

    def __init__(self, function, brief, description = None, **kwargs):
        self._brief = brief
        self._description = description
        self._meta = kwargs

        self._function = function
    
    async def execute(self, argv, kwargs):
        if callable(self._function):
            if iscoroutinefunction(self._function):
                return await self._function(*argv, **kwargs)
            else:
                return self._function(*argv, **kwargs)
        return utils.error_embed('Error.', 'Could not find a callable in the command object.')