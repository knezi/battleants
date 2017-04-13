#!/bin/env python3
import time
import os
import sys
from src.game import Game

if len(sys.argv)!=3:
    print("Please run as: ./main.py in_file out_file")
    sys.exit(1)

game=Game(sys.argv[1], sys.argv[2])
cont=True
while cont:

    for pl in game.get_players():
        kill=time.time()+game.get_timeout()
        pl[2].run(kill)
        # TODO kill at time kill

    cont=game.next_iteration()

res=[0 for x in range(game.no_players())]

for x,y,a in game.get_ants():
    res[a-1]+=1

win=0
for x in range(1,len(res)):
    if res[win]<res[x]:
        win=x

print("Winner is {}\n".format(game.get_players()[win][0]))
