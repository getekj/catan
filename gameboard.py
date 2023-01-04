# Author: Joanna Getek
# Last Modified: 01/03/2023
# Description: The creation of the board and buttons for gameplay. It contains the classes
# GameBoard, HexTile, and Location, as well as a method for printing text to be displayed

import math
import random
from global_vars import *

class GameBoard:
    """
    Create the game board for game play
    Center indicates the coordinates of the center of the board
    Hex_size indicates the size of each HexTile in pixels
    All of the lists contain objects of the class described in the name
    """
    def __init__(self):
        self._center = (425, 250)
        self._hex_size = 120
        self._list_hex_tiles = []
        self._list_locations = []
        self._player_list = []
        self._robber_hex_tile = None

    def create_hex_tiles(self):
        """
        Creates the 19 hexagon tiles that make up the game board
        """

        # Each tuple is matched with the tile colour and corresponding resource
        type_colours = [("wheat", YELLOW), ("wool", GREEN), ("wood", DARK_GREEN)] * 4
        type_colours += [("ore", GREY), ("brick", RED)] * 3

        hex_center_coord_list = [           (321, 100), (425, 100), (529, 100),
                                        (269, 190), (373, 190), (477, 190), (581, 190),
                                 (217, 280), (321, 280), (425, 280), (529, 280), (633, 280),
                                        (269, 370), (373, 370), (477, 370), (581, 370),
                                            (321, 460), (425, 460), (529, 460)               ]

        # each number will correspond to a number token on the HexTile
        numbers = ["2", "12"]
        numbers += ["3", "4", "5", "6", "8", "9", "10", "11"] * 2

        # shuffling to ensure the map is different for each game
        random.shuffle(type_colours)
        random.shuffle(hex_center_coord_list)
        random.shuffle(numbers)

        # Creating first 18 tile objects on the board, then creating desert last to ensure robber is on desert
        for index in range(18):
            hexagon = HexTile(type_colours[index], self._hex_size, hex_center_coord_list[index], numbers[index])
            self._list_hex_tiles.append(hexagon)

        # Creating desert tile
        desert_hexagon = HexTile(("desert", BEIGE), self._hex_size, hex_center_coord_list[18], "")
        self._list_hex_tiles.append(desert_hexagon)

        # adding robber to hexagon tile for initial location
        self.update_robber_tile(desert_hexagon)



class HexTile:
    """
    Creating a hexagon tile for the game board
    Each tile has a will have:
        a string for the resource type, corresponding colour, and number, which represents the dice roll token
        an int for the size for the tile in pixels
        a tuple representing the center coordinates
        a list that holds the coordinates of the 6 hexagon corners, the method create_coordinates generate this list
        a bool that indicates whether there is a robber on the space (True), otherwise will be False
    """
    def __init__(self, type_colour, size, center, number):
        self._type = type_colour[0]
        self._colour = type_colour[1]
        self._size = size
        self._center = center
        self._number = number
        self._coordinates = []
        self._robber = False

        # Uses the center coordinate to create the 6 hexagon corners
        self.create_coordinates(self._center)

    def get_center_coords(self):
        return self._center

    def get_robber(self):
        return self._robber

    def set_robber(self, robber_bool):
        self._robber = robber_bool

    def get_coordinates(self):
        return self._coordinates

    def get_number(self):
        return self._number

    def get_type(self):
        return self._type

    def create_coordinates(self, hex_center):
        """
        Creates the list of coordinates representing each hexagon corner used to generate the hexagon shape on the board
        Formula to calculate coordinates modified from: https://www.redblobgames.com/grids/hexagons/
        """

        x_coord = hex_center[0]
        y_coord = hex_center[1]
        alpha = self._size / 4
        beta = math.sqrt(3) * alpha

        self._coordinates.append((round(x_coord), round(y_coord - (2 * alpha))))
        self._coordinates.append((round(x_coord + beta), round(y_coord - alpha)))
        self._coordinates.append((round(x_coord + beta), round(y_coord + alpha)))
        self._coordinates.append((round(x_coord), round(y_coord + (2 * alpha))))
        self._coordinates.append((round(x_coord - beta), round(y_coord + alpha)))
        self._coordinates.append((round(x_coord - beta), round(y_coord - alpha)))

    def draw_hex(self):
        """
        Displays the hex tile to the screen surface
        """
        pygame.draw.polygon(screen, self._colour, self._coordinates)
        #print_text(self._number, (self._center[0] - 15, self._center[1] - 15))