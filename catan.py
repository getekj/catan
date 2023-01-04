# Author: Joanna Getek
# Last Modified: 01/03/2023
# Description: A 2D Catan board game with an interactive GUI for four players using the Pygame library.
# This file create the initial gameboard and generates the players. It also contains the main game loop.

# imports
import sys
import pygame
from global_vars import *
from gameboard import *

def start_game():
    """ Creates screen, GameBoard (and all its associated objects), and
     calls generate players to set up the initial game play"""

    # filling background
    screen.fill(LIGHT_BLUE)
    pygame.display.flip()

    # initializing GameBoard
    game = GameBoard()
    game.create_hex_tiles()
    game.create_locations()
    print(len(game.get_locations()))

def main():
    """ The initial setup and main game loop that continues to run as long as there is no winner or
    the user has not exited """

    game = start_game()
    winner = None

    while winner is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == '__main__':
    main()