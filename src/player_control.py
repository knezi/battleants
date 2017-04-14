class PlayerControl():
    """ interface for controlling ants and getting current state of the game
    this class can be accessed through self._pc in children of PlayerInstance
    for examples see players/*"""

    def __init__(self, no, game):
        """ no - number of this player
            game - instance of game object for accessing the game"""
        self._player=no
        self._game=game

    def get_player(self):
        """ return number of this player"""
        return self._player

    # interface for algorithms
    def move(self, x, y, x_new, y_new):
        """ move an ant at (x,y) to (x_new, y_new)
            it is only possible to change exactly one of the coordinates by exactly one;
            of course it is possible to move only player's own
            if the move is not permitted, nothing happens """
        if abs(x-x_new)+abs(y-y_new)!=1:
            return
    
        if x_new<0 or x_new>=self._game.get_width() or \
            y_new<0 or y_new>=self._game.get_height():
            return

        if self._game.get_square(x,y)==self._player and \
            self._game.get_square(x_new,y_new)>=0:
            self._game.move(x, y, x_new, y_new)

    def get_nest(self):
        """ return a tuple (x,y) of coordinates of the nest """
        return self._game.get_nest()

    def get_width(self):
        """ return a width of the arena """
        return self._game.get_width()

    def get_height(self):
        """ return a height of the arena """
        return self._game.get_height()

    def get_walls(self):
        """ return a BoxContainer containing all walls """
        return self._game.get_walls()

    def get_ants(self):
        """ return a BoxContainer containing both own and enemious ants """
        return self._game.get_ants()

    def get_timeout(self):
        """ return a time available for one iteration """
        return self._game.get_timeout()

    def get_square(self, x, y):
        """ return number of what is at coordinates (x,y):
            -1    wall
            0     nothin
            1...  ant belonging to player whose number it is"""
        return self._game.get_square(x, y)

    def get_iteration(self):
        """ return the number of current iteration (numbered from 1)"""
        return self._game.get_iteration()

    def no_iterations(self):
        """ return number of iterations in the game j"""
        return self._game.no_iterations()

    def no_players(self):
        """ return number of this player"""
        return self._game.no_players()

    def last_moves(self):
        """ return a BoxContainer containing all ants that has been moved in the last iteration in the format:
            for an ant that has moved from (x,y) to (xn,yn) the box contains a tuple (xn,yn) on the (x,y) position"""
        return self._game.last_moves()

    def last_kills(self):
        """ return a boxcontainer containing positions of all ants that has been killed in the last iteration"""
        return self._game.last_kills()
