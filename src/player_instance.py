import random

class PlayerInstance():
    def __init__(self, player_control):
        self._pc=player_control

    """ to be overwritten """
    def run(self, timeout):
        pass
