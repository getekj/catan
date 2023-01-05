# Author: Joanna Getek
# Last Modified: 01/02/2023
# Description: Contains the classes for building a player's roads, settlements and cities

import pygame
from global_vars import *

class Settlement:
    """
    Creates a settlement object on a location on the gameboard belonging to one of the players
    """
    def __init__(self, position, colour):
        self._position = position
        self._colour = colour
        self._surrounding_tiles = []
        self._victory_points = 1

    def get_position(self):
        return self._position

    def get_surrounding_tiles(self):
        return self._surrounding_tiles

    def create_surrounding_tiles(self, game):
        """
        Adds all tiles surrounding the settlement to self._surrounding_tiles
        """
        game_hex_tiles = game.get_hex_tiles()
        # iterate through each hex tile and get list of coordinates
        for hex_tile in game_hex_tiles:
            hex_coordinates = hex_tile.get_coordinates()
            # if the settlement position is a hex_tile coordinate, append the hex_tile object to surrounding tiles
            if self._position in hex_coordinates:
                self._surrounding_tiles.append(hex_tile)

    def draw_settlement(self):
        """
        Draws the settlement to the game screen
        """
        x = self._position[0]
        y = self._position[1]
        pentagon_coordinates = [(x - 10, y - 10), (x - 10, y + 10), (x + 10, y + 10), (x + 10, y - 10), (x, y - 20)]
        pygame.draw.polygon(screen, self._colour, pentagon_coordinates)
        pygame.display.flip()


class Road:
    """
    Takes as parameters:
        road coordinates, a list containing two tuples that contain the start and end coordinates of the road
        colour, a string indicating the colour of the road
    Creates a road object attached to two locations on the gameboard belonging to one of the players
    """
    def __init__(self, road_coordinates, colour):
        self._colour = colour
        self._start_pos = road_coordinates[0]
        self._end_pos = road_coordinates[1]

    def draw_road(self):
        """
        Draws a road to the game screen
        """
        pygame.draw.line(screen, self._colour, self._start_pos, self._end_pos, 8)
        pygame.display.flip()


class City(Settlement):
    """
    Creates a city object on a location on the gameboard belonging to one of the players
    Inherits from Settlement class
    """
    def __init__(self, position, colour):
        super().__init__(position, colour)
        self._victory_points = 2

    def get_victory_points(self):
        return self._victory_points