from src.player_instance import PlayerInstance
from random import *

class RandomPlayer(PlayerInstance):
    def __init__(self, *args):
        super().__init__(*args)
        self.it=0

    def run(self, kill):
        # print(random)
        # print(randint)
        self.it+=1
        if self.it%2:
            self._pc.move(0,3, 0,2)
        else:
            self._pc.move(0,2, 0,3)
        pass
