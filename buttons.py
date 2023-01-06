# Author: Joanna Getek
# Last Modified: 01/04/2023
# Description: Contains all the buttons which allow the player to select turn options

import pygame
import sys
import random
from global_vars import *


class Dice:
    """
    Creates the dice object that the user clicks at the start of each turn
    """
    def __init__(self):
        self._colour = RED
        self._rect = pygame.Rect(900, 425, 150, 76)

    def get_rect(self):
        return self._rect

    def draw_dice(self, dice_roll=2):
        """
        Displays two dice that indicate the dice number that was rolled
        """
        dice_image_location = "images\\dice" + str(dice_roll) + ".jpg"
        dice_image = pygame.image.load(dice_image_location).convert()
        screen.blit(dice_image, (900, 425))
        pygame.display.flip()

    def roll_dice(self):
        """
        Returns the dice roll when the button is clicked
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self._rect.collidepoint(x, y):
                        dice_roll = random.randint(2, 12)
                        return dice_roll


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

    def get_position(self):
        return self._position

    def draw_button(self):
        """
        Draws the button on the game screen
        """
        screen.blit(self._image, self._position)

class Settlement_Button(Button):
    """
    Creates a button on the board for players to purchase settlements on their turn
    """
    def __init__(self, colour=NAVY):
        super().__init__(colour)
        self._shape = pygame.Rect(1100, 315, 60, 65)
        self._image = pygame.image.load("images\\settlement_button1.jpg").convert()
        self._position = (1100, 315)

    def click_settlement_button(self, game, player):
        """
        When the button is clicked, it indicates player would like to build a settlement
        """
        player.place_settlement(game)

class Road_Button(Button):
    """
    Creates a button on the board for players to purchase roads on their turn
    """
    def __init__(self, colour=NAVY):
        super().__init__(colour)
        self._shape = pygame.Rect(1100, 250, 60, 65)
        self._image = pygame.image.load("images\\road_button1.jpg").convert()
        self._position = (1100, 250)

    def clicked_road_button(self, game, player):
        """
        Indicates player would like to build a road
        """
        player.place_road(game)

class City_Button(Button):
    """
    Creates a button on the board for players to purchase cities on their turn
    """
    def __init__(self, colour=NAVY):
        super().__init__(colour)
        self._shape = pygame.Rect(1100, 185, 60, 65)
        self._image = pygame.image.load("images\\city_button1.jpg").convert()
        self._position = (1100, 185)

class Development_Card(Button):
    """
    Creates a button allowing players to purchase a development cards
    """
    def __init__(self, colour=NAVY):
        super().__init__(colour)
        self._shape = pygame.Rect(1070, 405, 120, 183)
        self._image = pygame.image.load("images\\development_card.jpg").convert()
        self._position = (1070, 405)

class End_Turn(Button):
    """
    Creates a button object that allows the current player to end their turn
    """
    def __init__(self, colour=BEIGE):
        super().__init__(colour)
        self._shape = pygame.Rect(900, 525, 150, 50)
        self._position = (910, 535)

    def draw_button(self):
        """
        Draws the end turn button on the game board
        """
        pygame.draw.rect(screen, self._colour, self._shape)
        print_text = GAME_FONT.render("END TURN", True, BLACK)
        screen.blit(print_text, self._position)

    def click_end_turn_button(self):
        """
        When clicked, indicates player would like to end their turn
        """
        return True

class Wheat_Button(Button):
    """
    Creates a wheat button object that allows the player to trade in wheat for another resource
    """
    def __init__(self, colour=NAVY):
        super().__init__(colour)
        self._shape = pygame.Rect(860, 70, 65, 65)
        self._image = pygame.image.load("images\\wheat.jpg").convert()
        self._position = (860, 70)

    def clicked_wheat_button(self, player):
        """
        Takes the object player as a parameter
        Checks whether a player has enough resources to trade in 4 wheat cards, removes the cards if trade is valid
        """
        player_hand = player.get_resources()
        if player_hand["wheat"] < 4:
            # unable to trade
            return False

        # otherwise player is able to trade, 4 wheat cards are removed from player hand
        current_wheat = player_hand["wheat"]
        player_hand["wheat"] = current_wheat - 4
        return True



class Brick_Button(Button):
    """
    Creates a brick button object that allows the player to trade in brick for another resource
    """
    def __init__(self):
        self._shape = pygame.Rect(925, 70, 65, 65)
        self._image = pygame.image.load("images\\brick.jpg").convert()
        self._position = (925, 70)

    def clicked_brick_button(self, player):
        """
        Takes the object player as a parameter
        Checks whether a player has enough resources to trade in 4 brick cards, removes the cards if trade is valid
        """
        player_hand = player.get_resources()
        if player_hand["brick"] < 4:
            return False

        # otherwise player is able to trade, 4 brick cards are removed from player hand
        current_brick = player_hand["brick"]
        player_hand["brick"] = current_brick - 4
        return True


class Wood_Button(Button):
    """
    Creates a wood button object that allows the player to trade in wood for another resource
    """

    def __init__(self):
        self._shape = pygame.Rect(990, 70, 65, 65)
        self._image = pygame.image.load("images\\wood.jpg").convert()
        self._position = (990, 70)

    def clicked_wood_button(self, player):
        """
        Takes the object player as a parameter
        Checks whether a player has enough resources to trade in 4 wood cards, removes the cards if trade is valid
        """
        player_hand = player.get_resources()
        if player_hand["wood"] < 4:
            return False

        # otherwise player is able to trade, 4 wood cards are removed from player hand
        current_wood = player_hand["wood"]
        player_hand["wood"] = current_wood - 4
        return True

class Wool_Button(Button):
    """
    Creates a wool button object that allows the player to trade in wool for another resource
    """

    def __init__(self):
        self._shape = pygame.Rect(1055, 70, 65, 65)
        self._image = pygame.image.load("images\\wool.jpg").convert()
        self._position = (1055, 70)

    def clicked_wool_button(self, player):
        """
        Takes the object player as a parameter
        Checks whether a player has enough resources to trade in 4 wool cards, removes the cards if trade is valid
        """
        player_hand = player.get_resources()
        if player_hand["wool"] < 4:
            return False

        # otherwise player is able to trade, 4 wool cards are removed from player hand
        current_wool = player_hand["wool"]
        player_hand["wool"] = current_wool - 4
        return True

class Ore_Button(Button):
    """
    Creates a ore button object that allows the player to trade in ore for another resource
    """

    def __init__(self):
        self._shape = pygame.Rect(1120, 70, 65, 65)
        self._image = pygame.image.load("images\\ore.jpg").convert()
        self._position = (1120, 70)

    def clicked_ore_button(self, player):
        """
        Takes the object player as a parameter
        Checks whether a player has enough resources to trade in 4 ore cards, removes the cards if trade is valid
        """
        player_hand = player.get_resources()
        if player_hand["ore"] < 4:
            return False

        # otherwise player is able to trade, 4 wool cards are removed from player hand
        current_wool = player_hand["ore"]
        player_hand["ore"] = current_wool - 4
        return True

