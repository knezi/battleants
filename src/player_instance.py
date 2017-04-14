class PlayerInstance():
    """ algorithms of bots inherit from this class"""
    def __init__(self, player_control):
        """ this method must be called as the first thing in __init__ of the bot's algorithm"""
        self._pc=player_control

    def run(self, timeout):
        """ to be overwritten, executed once for every iteration """
        pass
