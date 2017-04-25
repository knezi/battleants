#!/bin/env python3
import unittest
from src.game import Game
from src.player_control import PlayerControl
from src.player_instance import PlayerInstance
from src.box_container  import BoxContainer
import src.exceptions as exceptions

class TestBoxContainer(unittest.TestCase):
    def testBoxContainer(self):
        bc=BoxContainer(5, 5)
        bc.insert(1,2,1)
        bc.insert(1,3,1)
        bc.insert(1,3,2)
        bc.insert(2,2,1)
        bc.remove(1,2)
        bc.remove(2,2)

        self.assertRaises(exceptions.OutOfRangeError, bc.insert, 6,6,1)

        self.assertEqual(list(bc), [(1,3,2)])
        self.assertEqual(bc.get(2,2), None)
        self.assertEqual(bc.get(1,3), 2)

        bc.clear()
        self.assertEqual(list(bc), [])

class TestGame(unittest.TestCase):
    def testInterface(self):
        testing=Game("arenas/testing", "arenas/testing_out")
        self.assertEqual(testing.get_iteration(), 1)
        self.assertEqual(testing.no_iterations(), 10)
        self.assertEqual(testing.get_timeout(), 2)
        self.assertEqual(testing.no_players(), 2)

        boxes=[(0,0, -1),
                (1,2, -1),
                (3,3, 0),
                (2,0, 1),
                (0,3, 2)]
        for x,y,val in boxes:
            self.assertEqual(testing.get_square(x, y), val)

        # |# xx|     |# x |
        # |  x | --> |  xx|
        # | # #| --> | # #|
        # |ooo |     |ooo |

        testing.move(2, 0,  2, 1)
        testing.move(2, 1,  2, 2)
        testing.move(3, 0,  3, 1)
        testing.move(2, 3,  2, 2)
        testing.move(0, 3,  1, 3)

        testing.next_iteration()

        boxes=[(0,0, -1),
                (1,2, -1),
                (3,3, 0),
                (2,0, 1),
                (2,1, 1),
                (0,3, 2)]
        for x,y,val in boxes:
            self.assertEqual(testing.get_square(x, y), val)


        self.assertEqual(testing.get_iteration(), 2)

        walls=testing.get_walls()
        self.assertEqual(walls.get(3,0), None)
        self.assertEqual(walls.get(3,2), -1)

        ants=testing.get_ants()
        self.assertEqual(ants.get(2,0), 1)
        self.assertEqual(ants.get(0,3), 2)
        self.assertEqual(ants.get(3,0), None)

        last_moves=testing.last_moves()
        self.assertEqual(last_moves.get(3,0), (3,1,1))
        self.assertEqual(last_moves.get(2,2), None)
        self.assertEqual(last_moves.get(0,3), None)

    def testCyclest(self):
        # not moving cycle
        testing=Game("arenas/testing_cycle", "arenas/testing_cycle_out")
        testing.move(0, 0,  1, 0)
        testing.move(1, 0,  1, 1)
        testing.move(1, 1,  0, 1)
        testing.move(0, 1,  0, 0)


        testing.next_iteration()

        self.assertEqual(testing.get_square(0, 0), 1)
        self.assertEqual(testing.get_square(1, 1), 1)
        self.assertEqual(testing.get_square(1, 0), 2)
        self.assertEqual(testing.get_square(0, 1), 2)

        # not moving cycle with additional "branches"
        testing=Game("arenas/testing_cycle", "arenas/testing_cycle_out2")
        testing.move(0, 0,  1, 0)
        testing.move(1, 0,  1, 1)
        testing.move(1, 1,  0, 1)
        testing.move(0, 1,  0, 0)
        testing.move(2, 0,  1, 0)
        testing.move(2, 1,  2, 0)

        testing.next_iteration()

        self.assertEqual(testing.get_square(0, 0), 1)
        self.assertEqual(testing.get_square(1, 1), 1)
        self.assertEqual(testing.get_square(1, 0), 2)
        self.assertEqual(testing.get_square(0, 1), 2)
        self.assertEqual(testing.get_square(2, 0), 1)
        self.assertEqual(testing.get_square(2, 1), 1)

    def testKill(self):
        testing=Game("arenas/testing_kills", "arenas/testing_kills_out")
        testing.next_iteration()

        self.assertEqual(list(testing.last_kills()), [(1, 0, 2)])
        self.assertEqual(testing.get_square(1, 0),  0)


class TestPlayer(unittest.TestCase):
    def testInterface(self):
        testing=Game("arenas/testing", "arenas/testing_out")

        self.assertEqual(testing.get_players()[0][2]._pc.get_iteration(), 1)
        self.assertEqual(testing.get_players()[0][2]._pc.no_iterations(), 10)
        self.assertEqual(testing.get_players()[0][2]._pc.get_timeout(), 2)
        self.assertEqual(testing.get_players()[0][2]._pc.no_players(), 2)

        boxes=[(0,0, -1),
                (1,2, -1),
                (3,3, 0),
                (2,0, 1),
                (0,3, 2)]
        for x,y,val in boxes:
            self.assertEqual(testing.get_players()[0][2]._pc.get_square(x, y), val)

        # |# xx|     |# x |
        # |  x | --> |  xx|
        # | # #| --> | # #|
        # |ooo |     |ooo |

        testing.get_players()[0][2]._pc.move(2, 0,  2, 1)
        testing.get_players()[0][2]._pc.move(2, 1,  2, 2)
        testing.get_players()[0][2]._pc.move(3, 0,  3, 1)
        testing.get_players()[1][2]._pc.move(2, 3,  2, 2)
        testing.get_players()[0][2]._pc.move(0, 3,  0, 2) # trying to move enemious ant

        testing.next_iteration()

        boxes=[(0,0, -1),
                (1,2, -1),
                (3,3, 0),
                (2,0, 1),
                (2,1, 1),
                (0,3, 2)]
        for x,y,val in boxes:
            self.assertEqual(testing.get_players()[0][2]._pc.get_square(x, y), val)


        self.assertEqual(testing.get_players()[0][2]._pc.get_iteration(), 2)

        walls=testing.get_players()[0][2]._pc.get_walls()
        self.assertEqual(walls.get(3,0), None)
        self.assertEqual(walls.get(3,2), -1)
        self.assertEqual(walls.get(2,2), None)

        ants=testing.get_players()[0][2]._pc.get_ants()
        self.assertEqual(ants.get(2,0), 1)
        self.assertEqual(ants.get(0,3), 2)
        self.assertEqual(ants.get(3,2), None)

        last_moves=testing.get_players()[0][2]._pc.last_moves()
        self.assertEqual(last_moves.get(3,0), (3,1,1))
        self.assertEqual(last_moves.get(0,0), None)
        self.assertEqual(last_moves.get(1,0), None)
        self.assertEqual(last_moves.get(2,0), None)




if __name__ == '__main__':
    unittest.main()
