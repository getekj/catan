# Author: Joanna Getek
# Last Modified: 01/03/2023
# Description: Global variables that are used among the files for catan project

import pygame

# Define screen constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 30
FONT_SIZE = 30
SMALL_FONT_SIZE = 15

# Initializing font
pygame.font.init()
GAME_FONT = pygame.font.SysFont('calibri', FONT_SIZE)
SMALL_FONT = pygame.font.SysFont('calibri', SMALL_FONT_SIZE)

# Define Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (217, 67, 35)
GREEN = (122, 217, 123)
GREY = (135, 135, 129)
YELLOW = (253, 255, 168)
BEIGE = (207, 185, 151)
DARK_GREEN = (23, 99, 30)
BLUE = (0, 153, 255)
LIGHT_BLUE = (204, 238, 255)
PURPLE = (153, 0, 204)
PINK = (255, 153, 255)
ORANGE = (255, 133, 51)
NAVY = (0, 0, 153)

# Define player constants
PLAYER_COLOUR_LIST = [BLUE, PINK, PURPLE, ORANGE]
PLAYER_POSITIONS = [(10, 10), (700, 10), (10, 360), (700, 360)]
RECT_PLAYER_POSITIONS = [(10, 40), (700, 40), (10, 390), (700, 390)]

# Initializing pygame and screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Creates caption for window
pygame.display.set_caption("Settlers of Catan Pygame")

# Ensures we are running at correct FPS - do we need?
#clock = pygame.time.Clock()
