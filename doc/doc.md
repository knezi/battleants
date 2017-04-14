# Arena for battles of ants armies

## What is it about

This is a little arena for bots written in python to compete with others. Every
player has got an army of ants in a classical maze with walls. The goal is to
have more ants after a fixed number of iterations than anyone else.

In every iteration any ant can be ordered by its master to move one field up,
down, to the left or right. All orders are stored in a buffer. When every bot
has given orders, conflicts are resolved and ants are moved.

Thereafter fights come. Every arena has specified a number of ants needed to
kill a foe. For every ant is checked how many enemies surround it (every field
excluding borders has eight neighbouring fields). If the number is at least the
number of needed kills, ant is immediately dead and removed from the arena.

Eventually, there can be born a new ant. If there is a nest and there is no one
standing on it, new ant appears on this field. It belongs to the player with
most ants surrounding the nest.

### Conflicts

Whenever an ant is to be moved, it is firstly checked whether the filed it is
moving to is free

* If so, and there is no one moving to this field at the same time, the ant is
  moved.

* If there is an ant that is not moving or is moving to the field of the
  current ant, no move is performed. 

* If there is an ant, but it is moving away, the current ant is moved.
  Therefore it must be checked whether the ant is not blocked by anyone else.
  This can lead to rather complicated situations.

For resolving complex situations a recursive approach is taken. Before deciding
whether a potentially blocking ant will move away, the same algorithm is simply
called for this ant recursively. By this we either end up finding an ant that
can be solved straight away (the first or second bullet) or a cycle occurs. If
the recursive function is called for an ant that is already in the stack, the
cycle has been find and in that case no ant can move. The situations bellow
should be self-explanatory.

	|--------| Every number represents an ant.
	|120     | Suppose the following moves:
	|43    # | 1 -> 2 (means ant no. 1 is going to the position of chararacter 2)
	|      5 | 2 -> 3; 3 -> 4; 4 -> 1; 0 -> 2
	|   9  6 | 5 -> #; 6 -> 5
	| 7.8    | 7 -> .; 8 -> .; 9 -> 8
	|--------| 

No one will move in this situation. Ants `1,2,3,4` create a cycle therefore
they don't move. `0` is blocked by `2`. `5` can't move because there is a wall
and therefore `6` is blocked by `5`. `7` and `8` goes to the same field and
therefore they cannot move and `9` is blocked `8` since it is not moving in
this iteration.


## Installation

### Dependencies

* PyQT 4 (needed just for the graphical visualisation)
* Python 3
* module [import\_file](https://pypi.python.org/pypi/import_file)- no need to
  install, comes prebundled

Additionally if you want to recompile documentation, you need `pandoc` and
`pydoc`.

### Compilation

The arena simulator itself does not need any compilation - just run
`./main.py`. For graphical visualisation run `make gui`. It can be executed by
`./src/gui/gui.py`.

### Running

Simply run by:

`./main.py in_file out_file`

where `in_file` is a valid file in the format described later. Run of the game
will be stored in `out_file`. It is possible to thereafter run:

`./src/gui/gui.py out_file`

to see visualisation of the game.

###  testing

There are unittest in file `test.py`. Tests can be run by executing `make test`.

## Format specification

### in file

	 "timeoutPerPlayer in secs" "numberOfIterations" "ants needed to kill"
	 width height of a maze x y of a nest (-1,-1 for no nest)
     
	 number of players name1 R1 G1 B1 path-to-file name-of-class antx1 anty1
	 ...  antxn antyn
     
	 name2 R2 G2 B2 path class antx1 anty1 ...  antxm antym
     
	 wallx1 wally1 ...  wallxm wallym
     

All fields are integers except of name of players which is string not containing
space. Path-to-file is where the class of bot's algorithm is stored and
name-of-class is the of class stored in this file. Please note a blank line at
the end of the file.

The file for each player looks like:

	from src.player_instance import PlayerInstance

	class Name(PlayerInstance): def __init__(self, *args):
	super().__init__(*args) # your code for initialization

		def run(self, kill): # your code run every iteration # move ant ant
		from (1,1) to (1,2) self._pc.move(1,1,1,2)
			

The class must inherit from PlayerInstance and call super method from
`__init__`. For controlling the game is used class PlayerControl available as a
private variable for each player with name `self._pc`. Detailed description can
be found in the programmer's documentation.


### out file

	 player1 R1 G1 B1 ...  playern Rn Gn Bn
     
	 wallx1 wally1 ..  wallxm wallym
     
	 pl antx anty ...  pl antx anty
     
	 pl antx anty ...  pl antx anty

   
Out\_file format is simple. First there is a list of players followed by a
blank line. Then specification of walls and then positions of all ants in every
iterations with iterations being split by a blank line.

## Programmer's documentation

The main flow of the programme is:

    game=Game("in", "out")

	while ...:
		for pl in game.get_players():
			pl.run()

		game.next_iteration()


Classes:

[Game](game.html)

[PlayerControl](player_control.html)

[PlayerInstance](player_instance.html)

[BoxContainer](box_container.html)

[Exceptions](exceptions.html)



TODO ACKNOLEDGHEKJASKFJASDKF AS    MFF HONZIK ATD
