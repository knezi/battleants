from src.player_instance import PlayerInstance
import random

class RandomPlayer(PlayerInstance):
    def __init__(self, *args):
        super().__init__(*args)
        self.me=self._pc.get_player()

    def run(self, kill):
        for x,y,a in self._pc.get_ants():
            x_new,y_new=x,y
            if a==self.me:
                if random.randint(1,2)==1:
                    if random.randint(1,2)==1:
                        x_new+=1
                    else:
                        x_new-=1
                else:
                    if random.randint(1,2)==1:
                        y_new+=1
                    else:
                        y_new-=1
                        
            self._pc.move(x,y,x_new,y_new)
