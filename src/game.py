from src.player_control import PlayerControl
from src.player_instance import PlayerInstance
from src.box_container import BoxContainer


class Game():
    def __init__(self, in_file, out_file):
        self._out_file=out_file
        try:
            with open(in_file, "r") as input:
                # load parameters
                self._timeout=int(input.readline())

                self._iterations=int(input.readline())
                self._current_iteration=1

                self._needed_to_kill=int(input.readline())

                self._width,self._height=(int(e) for e in input.readline().split(" "))

                self._moves_buffer=BoxContainer(self._width, self._height)
                # moves_buffer of previous iteration (not executed moves are skipped)
                self._last_moves=BoxContainer(self._width, self._height)
                self._died=BoxContainer(self._width, self._height)
                input.readline()


                # load Players
                self._players=[] # [name, (R, G, B), playerInstance]
                self._ants=BoxContainer(self._width, self._height)

                for curr_pl in range(1,int(input.readline())+1):
                    # create an instance of a player
                    line=input.readline().strip().split(" ")

                    pc=PlayerControl(curr_pl, self)
                    pi=PlayerInstance(pc) # TODO FOR ALGORITHMS
                    self._players.append([line[0], (int(e) for e in line[1:]), pi])

                    # create ants
                    line=input.readline().strip().split(" ")
                    while len(line)==2:
                        self._ants.insert(int(line[0]), int(line[1]), curr_pl)
                        line=input.readline().strip().split(" ")


                # load Walls
                self._walls=BoxContainer(self._width, self._height)
                line=input.readline().strip().split(" ")
                while len(line)==2:
                    self._walls.insert(int(line[0]), int(line[1]), -1)
                    line=input.readline().strip().split(" ") 

        except OSError as e:
            print("Problems reading input file {}\n".format(in_file))
            raise e

        # prepare out file
        with open(self._out_file, "w") as w:
            for pl in self._players:
                w.write("{} {} {} {}\n".format(pl[0], *pl[1]))
            w.write("\n")

            for x,y,_d in self._walls:
                w.write("{} {}\n".format(x,y))
            w.write("\n")



    """ Move an ant from x,y to x_new,y_new.
    Multiple moves of an ant are overwritten by the last one """
    def move(self, x, y, x_new, y_new):
        self._moves_buffer.insert(x,y,(x_new, y_new))

    """ flush buffer - execute possible moves & move onto the following iteration
        return: True  - keep going
                False - last iteration"""
    def next_iteration(self):
        # TODO test of impossible moves
        self._last_moves.clear()
        for x,y,(x_new,y_new) in self._moves_buffer:
            self._last_moves.insert(x, y, (x_new, y_new))
            self._ants.insert(x_new, y_new, self._ants.get(x, y))
            self._ants.remove(x,y)


        # prepare next iteration
        self._moves_buffer.clear()
        self._current_iteration+=1

        self._died.clear()
        for x,y,pl in self._ants:
            surr=0

            for i in range(-1,2):
                for j in range(-1,2):
                    if i==0 and j==0:
                        continue
                    a=self._ants.get(x+i,y+j)
                    surr+=1 if a!=None and a!=pl  else 0


            if surr>=self._needed_to_kill:
                self._ants.remove(x,y)
                self._died.insert(x,y,pl)
        

        # output current iteration
        with open(self._out_file, "a") as w:
            for x,y,pl in self._ants:
                w.write("{} {} {}\n".format(pl,x,y))
            w.write("\n")

        if self._current_iteration>self._iterations:
            return False
        return True

    # getters
    def get_walls(self):
        return self._walls

    def get_ants(self):
        return self._ants

    def get_timeout(self):
        return self._timeout

    def get_players(self):
        return self._players

    def get_square(self, x, y):
        w=self._walls.get(x,y)
        if w!=None:
            return w

        a=self._ants.get(x, y)
        if a!=None:
            return a

        return 0

    def get_iteration(self):
        return self._current_iteration

    def no_iterations(self):
        return self._iterations

    def no_players(self):
        return len(self._players)

    """ return a box container with moves executed in the last iteration """
    def last_moves(self):
        return self._last_moves

    def last_kills(self):
        return self._died


if __name__=="__main__":
    testing=Game("../arenas/testing", "../arenas/testing_out")
