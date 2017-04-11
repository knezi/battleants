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

        testing.next_iteration()
        # |# xx|     |# x |
        # |  x | --> |  xx|
        # | # #| --> | # #|
        # |ooo |     |ooo |

        testing.move(2, 0,  2, 1)
        testing.move(2, 1,  2, 2)
        testing.move(3, 0,  3, 1)
        testing.move(2, 3,  2, 2)
        testing.move(0, 3,  1, 3)


        boxes=[(0,0, -1),
                (1,2, -1),
                (3,3, 0),
                (2,0, 0),
                (2,1, 1),
                (0,3, 2)]
        for x,y,val in boxes:
            self.assertEqual(testing.get_square(x, y), val)


        self.assertEqual(testing.get_iteration(), 2)

        walls=testing.get_walls()
        self.assertEqual(walls[3][0], -1)
        self.assertEqual(walls[3][2], -1)
        self.assertNotTrue(2 in walls)

        ants=testing.get_ants()
        self.assertEqual(ants[2][0], 1)
        self.assertEqual(ants[0][3], 2)
        self.assertNotTrue(2 in ants[0])

        last_moved=testing.last_moved()
        self.assertEqual(last_moved[3][0], (1,3,1))
        self.assertNotTrue(0 in last_moved)
        self.assertNotTrue(1 in last_moved)
        self.assertNotTrue(2 in last_moved)

    def testCyclest(self):
        testing=Game("arenas/testing_cycle", "arenas_testing_cycle_out")
        testing.move(0, 0,  1, 0)
        testing.move(1, 0,  1, 1)
        testing.move(1, 1,  0, 1)
        testing.move(0, 1,  0, 0)
        testing.move(2, 0,  1, 0)
        testing.move(2, 1,  2, 0)

        testing.next_iteration()

        self.assertEqual(testing.get_square(0, 0), 2)
        self.assertEqual(testing.get_square(1, 1), 2)
        self.assertEqual(testing.get_square(1, 0), 1)
        self.assertEqual(testing.get_square(0, 1), 1)
        self.assertEqual(testing.get_square(2, 0), 1)
        self.assertEqual(testing.get_square(2, 1), 1)


class TestPlayer(unittest.TestCase):
    def testInterface(self):
        testing=Game("arenas/testing", "arenas/testing_out")

        player=PlayerControl(1, testing)
        self.assertEqual(player.get_player(), 1)
        playerInst=PlayerInstance(player)
        testing.add_player(playerInst)

        player=PlayerControl(2, testing)
        playerInst=PlayerInstance(player)
        testing.add_player(playerInst)

        self.assertEqual(testing.get_players()[0].get_iteration(), 1)
        self.assertEqual(testing.get_players()[0].no_iterations(), 10)
        self.assertEqual(testing.get_players()[0].get_timeout(), 2)
        self.assertEqual(testing.get_players()[0].no_players(), 2)

        boxes=[(0,0, -1),
                (1,2, -1),
                (3,3, 0),
                (2,0, 1),
                (0,3, 2)]
        for x,y,val in boxes:
            self.assertEqual(testing.get_players()[0].get_square(x, y), val)

        test.next_iteration()
        # |# xx|     |# x |
        # |  x | --> |  xx|
        # | # #| --> | # #|
        # |ooo |     |ooo |

        testing.get_players()[0].move(2, 0,  2, 1)
        testing.get_players()[0].move(2, 1,  2, 2)
        testing.get_players()[0].move(3, 0,  3, 1)
        testing.get_players()[1].move(2, 3,  2, 2)
        testing.get_players()[0].move(0, 3,  0, 2) # moving enemious ant


        boxes=[(0,0, -1),
                (1,2, -1),
                (3,3, 0),
                (2,0, 0),
                (2,1, 1),
                (0,3, 2)]
        for x,y,val in boxes:
            self.assertEqual(testing.get_players()[0].get_square(x, y), val)


        self.assertEqual(testing.get_players()[0].get_iteration(), 2)

        walls=testing.get_players()[0].get_walls()
        self.assertEqual(walls[3][0], -1)
        self.assertEqual(walls[3][2], -1)
        self.assertNotTrue(2 in walls)

        ants=testing.get_players()[0].get_ants()
        self.assertEqual(ants[2][0], 1)
        self.assertEqual(ants[0][3], 2)
        self.assertNotTrue(2 in ants[0])

        last_moved=testing.get_players()[0].last_moved()
        self.assertEqual(last_moved[3][0], (1,3,1))
        self.assertNotTrue(0 in last_moved)
        self.assertNotTrue(1 in last_moved)
        self.assertNotTrue(2 in last_moved)




if __name__ == '__main__':
    unittest.main()
