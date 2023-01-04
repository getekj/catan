# Author: Joanna Getek
# Last Modified: 01/04/2023
# Description: Contains all the buttons which allow the player to select turn options

from global_vars import *

class Button:
    """
    Creates a button object which allows a player to select the action to take for their turn
    """
    def __init__(self, colour=NAVY):
        self._colour = colour
        self._shape = None
        self._image = None
        self._position = None

    def get_shape(self):
        return self._shape

    def draw_button(self):
        """
        Draws the button on the game screen
        """
        screen.blit(self._image, self._position)

class Settlement_Button(Button):

    def __init__(self, colour=NAVY):
        """Creates a button on the board for players to purchase settlements on their turn"""
        super().__init__(colour)
        self._shape = pygame.Rect(1100, 315, 60, 65)
        self._image = pygame.image.load("images\\settlement_button1.jpg").convert()
        self._position = (1100, 315)


    def click_settlement_button(self, game, player):
        """
        When the button is clicked, it indicates player would like to build a settlement
        """
        locations = game.get_locations()
        player.place_settlement(locations, game)
