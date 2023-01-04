# Author: Joanna Getek
# Last Modified: 01/03/2023
# Description: Unit tests for catan project

import unittest
from global_vars import *
from gameboard import GameBoard, HexTile, Location

class CatanTester(unittest.TestCase):
    """Contains the unit tests for CatanTester"""
    def test1(self):
        """Testing GameBoard and Location initialization, get and set methods"""
        game = GameBoard()
        game.create_hex_tiles()
        game.create_locations()
        self.assertEqual(54, len(game.get_locations()))
        loc_coords = []
        for loc in game.get_locations():
            loc_coords.append(loc.get_x_y_coords())
        self.assertIn((373, 250), loc_coords)

        loc1 = Location(100, 100)
        loc1.set_road_bool()
        self.assertEqual(loc1.get_x_y_coords(), (100, 100))
        self.assertEqual(loc1.get_road_bool(), True)
        self.assertEqual(loc1.get_settlement_bool(), False)


    def test2(self):
        """Testing HexTile initialization, get and set methods"""
        hex1 = HexTile(("wheat", YELLOW), 100, (373, 370), "9")
        self.assertEqual(hex1.get_type(), "wheat")
        self.assertEqual(hex1.get_number(), "9")
        self.assertEqual(hex1.get_center_coords(), (373, 370))
        self.assertEqual(hex1.get_coordinates(), [(373, 320), (416, 345), (416, 395), (373, 420), (330, 395), (330,345)])


if __name__ == '__main__':
    unittest()