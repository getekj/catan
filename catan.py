# Author: Joanna Getek
# Last Modified: 01/03/2023
# Description: A 2D Catan board game with an interactive GUI for four players using the Pygame library.
# This file create the initial gameboard and generates the players. It also contains the main game loop.

# imports
import sys
import pygame
from global_vars import *
from gameboard import *
from buttons import *
from structures import *
from player import *

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
    game.create_buttons()

    # draw gameboard
    game.draw_gameboard()
    pygame.display.flip()

    # generate players and start initial setup
    generate_players(game)

    return game

def generate_players(game):
    """
    Takes game, the GameBoard object, and locations, the list of buildable locations on the board as parameters
    Creates four players for gameplay and starts their initial two turns for game setup
    """

    player_list = []

    # creating player list array, displaying names, and background
    for index in range(1, 5):
        player_name = "Player " + str(index)
        new_player = Player(player_name, PLAYER_COLOUR_LIST[index - 1])
        print_text(player_name, PLAYER_POSITIONS[index - 1])
        player_list.append(new_player)
        new_player.set_player_rect(RECT_PLAYER_POSITIONS[index - 1])

    game.set_player_list(player_list)
    game.draw_settlement_icons()

    # First round of settlements to add onto game board in order from player 1 - 4
    for new_player in player_list:
        game.update_text_box(str(new_player.get_player_name()) + ": Place your settlement")
        new_player.place_settlement(game)
        game.update_text_box(str(new_player.get_player_name()) + ": Place your road")
        new_player.place_road(game)

    # Now add second set of settlements/roads in reverse order
    player_list.reverse()

    for player in player_list:
        game.update_text_box(str(player.get_player_name()) + ": Place your settlement")
        player.place_settlement(game)
        game.update_text_box(str(player.get_player_name()) + ": Place your road")
        player.place_road(game)

    # bringing back to original order
    player_list.reverse()

def main():
    """ The initial setup and main game loop that continues to run as long as there is no winner or
    the user has not exited """

    game = start_game()
    winner = None

    while winner is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # loop through each player turn until there is a winner
        player_list = game.get_player_list()
        for player in player_list:
            player_name = player.get_player_name()
            game.update_text_box(str(player_name) + "'s Turn. Click to roll the dice!")
            player.player_turn(game, player)
            #game.check_winner

if __name__ == '__main__':
    main()