class PlayerInstance():
    """ algorithms of bots inherit from this class"""
    def __init__(self, player_control):
        """ don't overwrite this, initialization can be done in start """
        self._pc=player_control
    
    def start(self):
        """ to be overwritten, executed once at the beginning """
        pass

    def run(self, timeout):
        """ to be overwritten, executed once for every iteration """
        pass
