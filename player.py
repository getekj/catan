# Author: Joanna Getek
# Last Modified: 01/04/2023
# Description: Contains the player class and associated methods for game play

import pygame
import sys
from global_vars import *
from structures import *


class Player:
    """
    This class creates a Player object for gameplay, with a maximum of 4 players
    Player name is a string representing the user's name
    Colour is a string representing of the player's structures
    Resources is a dictionary where the key is the name of the resource and the value is the number of resources of
    that type
    Settlements is the list of settlements objects that the player currently owns
    Roads is the list of road objects that the player currently owns
    Cities is a list of the cities objects that the player currently owns
    Victory points is an integer representing the amount of points the player currently has
    Player rect is an object created from the pygame library that represents the square display of the player's stats
    """
    def __init__(self, player_name, colour):
        self._player_name = player_name
        self._colour = colour
        self._resources = {"wheat": 0, "brick": 0, "wood": 0, "wool": 0, "ore": 0}
        self._settlements = []
        self._roads = []
        self._cities = []
        self._victory_points = 0
        self._player_rect = None

    def get_player_name(self):
        return self._player_name

    def get_player_colour(self):
        return self._colour

    def get_resources(self):
        return self._resources

    def get_victory_points(self):
        return self._victory_points

    def get_player_rect(self):
        return self._player_rect

    def set_player_rect(self, position):
        self._player_rect = pygame.Rect(position, (150, 200))
        self.draw_player_rect()

    def draw_player_rect(self):
        pygame.draw.rect(screen, BEIGE, self._player_rect)

    def place_settlement(self, game):
        """
        The player clicks on a position on the board to place a settlement and build_settlement is called to
        create the settlement at the selected location
        """
        settlement_locations = game.get_locations()

        # Loop to wait for player to click on a buildable location to place their settlement
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                for location in settlement_locations:
                    # location is the object, need x,y coordinate of location
                    coordinates = location.get_x_y_coords()
                    distance_x = coordinates[0] - event.pos[0]
                    distance_y = coordinates[1] - event.pos[1]
                    # Checking if the mouse click is nearby a potential settlement location
                    if distance_x > -10 and distance_x < 10 and distance_y > -10 and distance_y < 10:
                        self.build_settlement(coordinates, self._colour, game, location)
                        # update location to indicate a settlement is now there
                        location.set_settlement_bool()
                    else:
                        # if the current coordinate in the list is not a match, continue searching through the list
                        continue
                    return

    def build_settlement(self, position, colour, game, location):
        """
        Creates a new settlement on the board if there are no direct neighbours nearby, calls on check_to_build_settlement
        to ensure the settlement is being placed on a buildable location
        """

        # Checking if settlement is not on a direct neighbour location
        bool_build_settlement = self.check_to_build_settlement(location)

        if bool_build_settlement is True:
            new_settlement = Settlement(position, colour)
            new_settlement.create_surrounding_tiles(game)
            new_settlement.draw_settlement()
            self._settlements.append(new_settlement)
            self.add_victory_point(1)
        else:
            # otherwise, go back to place_settlement to wait for new mouse click
            self.place_settlement(game)

        # only want to update screen after initial game setup
        # if len(self._settlements) > 2:
        game.display_player_screen()

    def check_to_build_settlement(self, location):
        """
        Takes as parameter the location object, the potential building location
        Checks if the player has enough resources to buy a settlement and that there are no direct neighbours
            *UNLESS the settlement is placed during initial setup in which case only the neighbours are checked*
        If the player can build the settlement, it removes the resources from the player hand and returns True
        Returns False otherwise
        """

        # checking whether there is a neighbour one line away
        neighbours_list = location.get_neighbours_list()
        for neighbour in neighbours_list:
            if neighbour.get_settlement_bool() is True:
                return False

        # checking if player has enough resources to buy a settlement
        player_hand = self._resources
        for key in player_hand:
            if (key == "wheat" or key == "brick" or key == "wood" or key == "wool") and player_hand[key] < 1:
                # if we are in the initial set up, no resources are removed
                if len(self._settlements) < 2:
                    return True
                return False

        # remove the resources for payment to build settlement
        for key in player_hand:
            if key == "wheat" or key == "brick" or key == "wood" or key == "wool":
                resource_value = player_hand[key]
                player_hand[key] = resource_value - 1

        return True

    def add_victory_point(self, number_of_points):
        """
        Takes an integer, number_of_points, as the parameter
        Updates the number of victory points a player has currently
        """
        self._victory_points += number_of_points