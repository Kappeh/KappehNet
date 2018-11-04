import src.utils as utils

class Command():

    _brief = None
    _description = None
    _meta = {}

    def __getitem__(self, i):
        if i in self._meta:
            return self._meta[i]
        return None
    
    def get_help(self, description = False):
        if description and self._description:
            return self._description
        elif self._brief:
            return self._brief
        return utils.error_embed('Error.', 'Could not find command\'s help message.')