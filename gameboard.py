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

    def get_locations(self):
        return self._list_locations

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
        #self.update_robber_tile(desert_hexagon)

    def create_locations(self):
        """
        Creates all possible Location objects that settlements and roads can be placed on the board
        """

        location_points = []

        # iterate through all hexagon coordinates, create a location point as long as it is not a duplicate as some
        # hexagon corners overlap
        for hex_tile in self._list_hex_tiles:
            single_hex_coords = hex_tile.get_coordinates()
            for coord in single_hex_coords:
                if coord not in location_points:
                    location_points.append(coord)

        # iterate through list of all possible location points on board and create a Location object for each
        for location_coords in location_points:
            point = Location(location_coords[0], location_coords[1])
            self._list_locations.append(point)

        # create neighbours for each location to keep track of the adjacent spaces
        self.create_location_neighbours()

    def create_location_neighbours(self):
        """
        Create the neighbouring location points to ensure settlements and cities cannot be placed next to each other
        and roads are being placed to other roads or structures
        """

        # iterate through the list of locations on game board
        for location in self._list_locations:
            neighbour_locations = []
            loc_x, loc_y = location.get_x_y_coords()
            # iterate through each location checking if they are potentially a neighbour
            for neighbour_location in self._list_locations:
                neigh_x, neigh_y = neighbour_location.get_x_y_coords()
                # if the neighbours are within range of original location, will be added to the neighbour list
                if (neigh_x > loc_x - 5 and neigh_x < loc_x + 5) and (neigh_y > loc_y - 65 and neigh_y < loc_y + 65):
                    neighbour_locations.append(neighbour_location)
                elif (neigh_x > loc_x - 60 and neigh_x < loc_x + 60) and (neigh_y > loc_y - 35 and neigh_y < loc_y + 35):
                    neighbour_locations.append(neighbour_location)
            location.set_neighbours_list(neighbour_locations)


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


class Location:
    """
    Creates a location object that represents one of the possible "buildable" points, where a player is allowed
    to place a settlement or city. A player may place a road that is attached to two adjacent locations.
    x_coord and y_coord are integers representing the location x and y coordinates
    neighbour_list is a list of all adjacent locations one space away
    bool_road, bool_settlement, and bool_city will be True if the corresponding object is on the location, False otherwise
    """

    def __init__(self, x_coord, y_coord):
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._neighbours_list = []
        self._bool_road = False
        self._bool_settlement = False
        self._bool_city = False

    def set_road_bool(self):
        self._bool_road = True

    def get_road_bool(self):
        return self._bool_road

    def get_x_y_coords(self):
        return self._x_coord, self._y_coord

    def get_settlement_bool(self):
        return self._bool_settlement

    def set_settlement_bool(self):
        self._bool_settlement = True

    def get_neighbours_list(self):
        return self._neighbours_list

    def set_neighbours_list(self, list_of_neighbours):
        self._neighbours_list = list_of_neighbours
