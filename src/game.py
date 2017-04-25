from src.player_control import PlayerControl
from import_file import import_file
from src.player_instance import PlayerInstance
from src.box_container import BoxContainer
from import_file.import_file import import_file


class Game():
    """ Class that handles logic of the game"""
    def __init__(self, in_file, out_file):
        """ in_file - arena in the correct input fromat
            out_file - the output file of the game"""
        self._out_file=out_file
        try:
            with open(in_file, "r") as input:
                # load parameters
                self._timeout=int(input.readline())

                self._iterations=int(input.readline())
                self._current_iteration=1

                self._needed_to_kill=int(input.readline())

                self._width,self._height=tuple(int(e) for e in input.readline().strip().split(" "))
                self._nest=tuple(int(e) for e in input.readline().strip().split(" ")) #-1,-1 for no nest

                self._moves_buffer=BoxContainer(self._width, self._height)
                self._seen=BoxContainer(self._width, self._height)
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
                    algo=input.readline().strip().split(" ")

                    algo_class=import_file(algo[0]).__dict__[algo[1]]

                    pc=PlayerControl(curr_pl, self)
                    pi=algo_class(pc)
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

        for _,_,x in self._players:
            x.start()

        # prepare out file
        with open(self._out_file, "w") as w:
            for pl in self._players:
                w.write("{} {} {} {}\n".format(pl[0], *pl[1]))
            w.write("\n")

            for x,y,_d in self._walls:
                w.write("{} {}\n".format(x,y))
            w.write("\n")

            for x,y,pl in self._ants:
                w.write("{} {} {}\n".format(pl,x,y))
            w.write("\n")


    def move(self, x, y, x_new, y_new):
        """ Move an ant from x,y to x_new,y_new.
        Multiple moves of an ant are overwritten by the last one
        It doesn't check whether a move is correct (this is done by PlayerControl)"""
        self._moves_buffer.insert(x,y,(x_new, y_new))

    def _dfs_free_moves(self, x, y):
        """ recursively decide whether x,y is to be moved
            return: False   was not moved
                    True    was moved """
        if self._seen.get(x, y)==1:
            return False # still in the stack -> cycle
        elif self._seen.get(x, y)==2:
            return True if self._moves_buffer.get(x,y)!=None else False
        self._seen.insert(x,y,1)

        col=[]
        x_new,y_new=self._moves_buffer.get(x,y)
        for i,j in ((-1,0), (1,0), (0,-1), (0,1)):
            if x_new+i>=0 and x_new+i<self._width and \
                y_new+j>=0 and y_new+j<self._height and \
                self._moves_buffer.get(x_new+i,y_new+j)==(x_new,y_new):
                col.append((x_new+i, y_new+j))

        # print(x,y,col,x_new,y_new)

        if self._ants.get(x_new, y_new)==None:
            target_free=True
        else:
            target_move=self._moves_buffer.get(x_new, y_new)
            #  target stays          wants goes against     is already seen -> cycle  
            if target_move==None or target_move==(x,y):
                target_free=False
            else:
                # print("CALLING {} {}".format(x_new,y_new))
                target_free=self._dfs_free_moves(x_new, y_new)
                # print(target_free)

        self._seen.insert(x,y,2)
        if len(col)==1 and target_free:
            self._last_moves.insert(x, y, (x_new, y_new, self._ants.get(x,y)))
            return True
        else:
            for x_rem,y_rem in col:
                self._moves_buffer.remove(x_rem, y_rem)
            return False


    def next_iteration(self):
        """ flush buffer - execute possible moves & move onto the following iteration:
            kill ants
            make a newborn
            return: True  - keep going
                    False - last iteration"""
        self._last_moves.clear()
        self._seen.clear()
        for x,y,(x_new,y_new) in self._moves_buffer:
            # BoxContainer does not mind if we remove some values while iterating
            self._dfs_free_moves(x, y)

        # update current position of ants
        # must be done in two phases - otherwise we can incidentally erase an ant
        for x,y,(x_new,y_new,pl) in self._last_moves:
            self._ants.remove(x,y)
        for x,y,(x_new,y_new,pl) in self._last_moves:
            self._ants.insert(x_new, y_new, pl)

        # prepare next iteration
        self._moves_buffer.clear()
        self._current_iteration+=1

        # kills
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
                self._died.insert(x,y,pl)

        for x,y,_ in self._died:
            self._ants.remove(x,y)

        # newborns
        if self._nest[0]!=-1 and self._ants.get(*self._nest)==None:
            pl=[0 for x in range(self.no_players()+1)]
            for x in range(-1,2):
                for y in range(-1,2):
                    a=self._ants.get(self._nest[0]+x,self._nest[1]+y)
                    if a!=None:
                        pl[a]+=1

            bestpl=0
            for x in range(1,len(pl)):
                if pl[bestpl]<pl[x]:
                    bestpl=x

            if bestpl!=0:
                self._ants.insert(*self._nest, bestpl)
        

        # output current iteration
        with open(self._out_file, "a") as w:
            for x,y,pl in self._ants:
                w.write("{} {} {}\n".format(pl,x,y))
            w.write("\n")

        if self._current_iteration>self._iterations:
            return False
        return True

    # getters
    def get_nest(self):
        """ return a tuple (x,y) of coordinates of the nest """
        return self._nest

    def get_width(self):
        """ return a width of the arena """
        return self._width

    def get_height(self):
        """ return a height of the arena """
        return self._height

    def get_walls(self):
        """ return a BoxContainer containing all walls """
        return self._walls

    def get_ants(self):
        """ return a BoxContainer containing both own and enemious ants """
        return self._ants

    def get_timeout(self):
        """ return a time available for one iteration """
        return self._timeout

    def get_players(self):
        return self._players

    def get_square(self, x, y):
        """ return number of what is at coordinates (x,y):
            -1    wall
            0     nothin
            1...  ant belonging to player whose number it is"""
        w=self._walls.get(x,y)
        if w!=None:
            return w

        a=self._ants.get(x, y)
        if a!=None:
            return a

        return 0

    def get_iteration(self):
        """ return the number of current iteration (numbered from 1)"""
        return self._current_iteration

    def no_iterations(self):
        """ return number of iterations in the game"""
        return self._iterations

    def no_players(self):
        return len(self._players)

    def last_moves(self):
        """ return a BoxContainer containing all ants that has been moved in the last iteration in the format:
            the box contains a tuple (xn,yn,pl) on the (x,y) position
            for an ant beloning to player no pl that has moved from (x,y) to (xn,yn)"""
        return self._last_moves

    def last_kills(self):
        """ return a boxcontainer containing positions of all ants that has been killed in the last iteration"""
        return self._died
