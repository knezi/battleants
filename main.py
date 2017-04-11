#!/bin/env python3
import time
from src.game import Game
game=Game("arenas/testing", "arenas/testing_out")

cont=True
while cont:

    for pl in game.get_players():
        kill=time.time()+game.get_timeout()
        pl[2].run(kill)
        # TODO kill at time kill

    cont=game.next_iteration()
