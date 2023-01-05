# Author: Joanna Getek
# Last Modified: 01/03/2023
# Description: Unit tests for catan project

import unittest
from global_vars import *
from gameboard import GameBoard, HexTile, Location
from buttons import *
from structures import *

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

    def test3(self):
        """Testing the Button classes initialization"""
        settlement_button = Settlement_Button()
        self.assertEqual(settlement_button.get_shape(), pygame.Rect(1100, 315, 60, 65))
        wheat_button = Wheat_Button()
        self.assertEqual(wheat_button.get_position(), (860, 70))

    def test4(self):
        """Testing the Settlement, Road, and City class initialization and methods"""
        game = GameBoard()
        game.create_hex_tiles()
        game.create_locations()
        settlement1 = Settlement((321, 40), RED)
        settlement1.create_surrounding_tiles(game)
        self.assertEqual(settlement1.get_position(), (321, 40))
        surrounding_tiles = settlement1.get_surrounding_tiles()
        self.assertEqual(surrounding_tiles[0].get_coordinates(), [(321, 40), (373, 70), (373, 130), (321, 160), (269, 130), (269, 70)])
        city1 = City((234, 456), ORANGE)
        self.assertEqual(city1.get_victory_points(), 2)
        self.assertEqual(city1.get_surrounding_tiles(), [])




if __name__ == '__main__':
    unittest()