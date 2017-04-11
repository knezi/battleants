class PlayerControl():
    def __init__(self, no, game):
        self._player=no
        self._game=game

    def get_player(self):
        return self._player

    # interface for algorithms
    def move(self, x, y, x_new, y_new):
        # my ant
        if self._game.get_square(x,y)==self._player:
            self._game.move(x, y, x_new, y_new)

    def get_walls(self):
        return self._game.get_walls()

    def get_ants(self):
        return self._game.get_ants()

    def get_timeout(self):
        return self._game.get_timeout()

    def get_square(self, x, y):
        return self._game.get_square(x, y)

    def get_iteration(self):
        return self._game.get_iteration()

    def no_iterations(self):
        return self._game.no_iterations()

    def no_players(self):
        return self._game.no_players()

    def last_moves(self):
        return self._game.last_moves()

    def last_kills(self):
        return self._game.last_kills()
