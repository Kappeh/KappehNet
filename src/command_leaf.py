from inspect import iscoroutinefunction
from src.command import Command

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
        return 'Error. could not find a callable in the command object.'