# Author: Joanna Getek
# Last Modified: 01/04/2023
# Description: Contains the player class and associated methods for game play

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
        self._resources = {"wheat": 2, "brick": 4, "wood": 4, "wool": 2,
                           "ore": 0}  # start player with two of each settlement resources so can build on inital turn
        self._settlements = []
        self._roads = []
        self._cities = []
        self._victory_points = 0
        self._player_rect = None