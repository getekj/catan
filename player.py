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

    def get_player_settlements(self):
        return self._settlements

    def get_player_roads(self):
        return self._roads

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

    def player_turn(self, game, player):
        """
        Player starts the turn by rolling the dice then clicking one of the buttons to indicate their desired action
        Takes the GameBoard and Player objects as parameters
        """

        # Start the turn by rolling the dice and displaying the roll to the screen
        dice = game.get_dice()
        dice_roll = dice.roll_dice()
        dice.draw_dice(dice_roll)

        # If a 7 was rolled, need to call robber_rolled to move the robber
        if dice_roll == 7:
            self.robber_rolled(game, player)
        else:
            # Otherwise collect resources from the roll
            self.collect_resources_from_roll(dice_roll, game)

        # Update instructions to player
        game.update_text_box(str(player.get_player_name()) + ", Click an icon to chose an action")
        game.update_trade_text("Select which item you'd like to trade in")

        # Now we loop waiting for player to select an action button, the loop ends when player selects end turn
        end_turn = False
        while end_turn is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    # monitoring if player selected a build structure or end turn button
                    build_buttons = game.get_build_buttons()

                    settlement_shape = build_buttons["settlement_button"].get_shape()
                    if settlement_shape.collidepoint(mouse_x, mouse_y):
                        build_buttons["settlement_button"].click_settlement_button(game, player)

                    road_shape = build_buttons["road_button"].get_shape()
                    if road_shape.collidepoint(mouse_x, mouse_y):
                        build_buttons["road_button"].clicked_road_button(game, player)

                    end_turn_shape = build_buttons["end_turn"].get_shape()
                    if end_turn_shape.collidepoint(mouse_x, mouse_y):
                        end_turn = build_buttons["end_turn"].click_end_turn_button()

                    # monitoring if player selected trade button
                    trade_buttons = game.get_trade_buttons()
                    trade_status = False

                    if trade_buttons["wheat"].get_shape().collidepoint(mouse_x, mouse_y):
                        trade_status = trade_buttons["wheat"].clicked_wheat_button(player)
                    elif trade_buttons["brick"].get_shape().collidepoint(mouse_x, mouse_y):
                        trade_status = trade_buttons["brick"].clicked_brick_button(player)
                    elif trade_buttons["wood"].get_shape().collidepoint(mouse_x, mouse_y):
                        trade_status = trade_buttons["wood"].clicked_wood_button(player)
                    elif trade_buttons["wool"].get_shape().collidepoint(mouse_x, mouse_y):
                        trade_status = trade_buttons["wool"].clicked_wool_button(player)
                    elif trade_buttons["ore"].get_shape().collidepoint(mouse_x, mouse_y):
                        trade_status = trade_buttons["ore"].clicked_ore_button(player)

                    if trade_status is True:
                        print("Which item would you like in return?")
                        game.update_trade_text("Select which item you'd to receive")
                        self.trade_cards(trade_status, game, player)
                        game.update_trade_text("Select which item you'd like to trade in")
                        trade_status = False

    def trade_cards(self, trade_status, game, player):

        trade_buttons = game.get_trade_buttons()

        while trade_status is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    trade_mouse_x, trade_mouse_y = event.pos

                    if trade_buttons["wheat"].get_shape().collidepoint(trade_mouse_x, trade_mouse_y):
                        current_wheat = self._resources["wheat"]
                        self._resources["wheat"] = current_wheat + 1
                    elif trade_buttons["brick"].get_shape().collidepoint(trade_mouse_x, trade_mouse_y):
                        current_brick = self._resources["brick"]
                        self._resources["brick"] = current_brick + 1
                    elif trade_buttons["wood"].get_shape().collidepoint(trade_mouse_x, trade_mouse_y):
                        current_wood = self._resources["wood"]
                        self._resources["wood"] = current_wood + 1
                    elif trade_buttons["wool"].get_shape().collidepoint(trade_mouse_x, trade_mouse_y):
                        current_wool = self._resources["wool"]
                        self._resources["wool"] = current_wool + 1
                    elif trade_buttons["ore"].get_shape().collidepoint(trade_mouse_x, trade_mouse_y):
                        current_ore = self._resources["ore"]
                        self._resources["ore"] = current_ore + 1

                    game.display_player_screen(self._player_name)

    def collect_resources_from_roll(self, dice_roll, game):
        """
        Iterates through all the players settlements and retrieves the surrounding hextiles
        If the number on the hex tile is equal to the dice roll and there is no robber on the tile,
        the player will collect the resource corresponding to the hex tile type
        """
        player_list = game.get_player_list()
        for player in player_list:
            player_settlement_list = player.get_player_settlements()
            for settlement in player_settlement_list:
                surrounding_tiles = settlement.get_surrounding_tiles()
                for hex_tile in surrounding_tiles:
                    number = hex_tile.get_number()
                    resource_type = hex_tile.get_type()
                    if number == dice_roll:
                        # if there is a robber at this hex tile will not collect any resources
                        if hex_tile.get_robber() is True:
                            return
                        else:
                            player.collect_resource(resource_type, game)

    def collect_resource(self, resource, game):
        """
        Updates player's hand by increasing the passed resource by 1
        """
        for key in self._resources:
            if key == resource:
                value = self._resources[key]
                self._resources[key] = value + 1
        game.display_player_screen(self._player_name)

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

        Takes as parameters:
            position - a tuple indicating the center coordinate of the new settlement
            colour - a string indicating the colour of the settlement
            game - the GameBoard object
            location - the location object where we are building the settlement
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

        # update screen with new resource and victory point count
        game.display_player_screen(self._player_name)

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

    def place_road(self, game):
        """
        The player clicks on a position on the board to place a road and build_road is called to create the road
        at the selected location
        """

        road_locations = game.get_locations()

        # while loop to wait for user click to indicate new road location
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                road_coordinates = []
                coordinate_locations = []
                for location in road_locations:
                    # location is the object, need x,y coordinate of location
                    coordinates = location.get_x_y_coords()
                    distance_x = coordinates[0] - event.pos[0]
                    distance_y = coordinates[1] - event.pos[1]
                    # Checking if the mouse click is nearby a potential road location
                    if distance_x > -40 and distance_x < 40 and distance_y > -40 and distance_y < 40:
                        road_coordinates.append(coordinates)
                        coordinate_locations.append(location)
                        # once we have two viable road coordinates, we can build the road inbetween
                        if len(road_coordinates) == 2:
                            self.build_road(road_coordinates, self._colour, game, coordinate_locations)
                            # Updating location objects to indicate a road is on the spot
                            coordinate_locations[0].set_road_bool()
                            coordinate_locations[1].set_road_bool()
                            return
                        # Need to continue searching for the second coordinate that is nearby to place road inbetween
                        continue
                    else:
                        # if the current coordinate in the list is not a match, continue searching through the list
                        continue
                    #return

    def build_road(self, position, colour, game, coordinate_locations):
        """
        Creates a new road on the board, calls on check_to_build_road to ensure that the road is being placed
        on a buildable location

        Takes as parameters:
            position - a list of two tuples indicating the two end coordinates of the new road
            colour - a string indicating the colour of the road
            game - the GameBoard object
            coordinate_locations - a list of the two location objects where we are building the road in between
        """

        bool_build_road = self.check_to_build_road(coordinate_locations)
        if bool_build_road is True:
            new_road = Road(position, colour)
            new_road.draw_road()
            self._roads.append(new_road)
        else:
            # not able to build in this location and need to wait for user to click on new location
            self.place_road(game)

        game.display_player_screen(self._player_name)

    def check_to_build_road(self, coordinate_locations):
        """
        Takes as parameter a list of two location objects, the potential road location
        Checks if the player has enough resources to buy a road and that there is another road or settlement at the
        location to attach to
            *UNLESS the settlement is placed during initial setup in which case we don't check or remove the resources*
        If the player can build the road, it removes the resources from the player hand and returns True
        Returns False otherwise
        """

        # checking to see if there is already a connected road or settlement at the point
        if coordinate_locations[0].get_road_bool() is False and coordinate_locations[
            0].get_settlement_bool() is False and \
                coordinate_locations[1].get_road_bool() is False and coordinate_locations[
            1].get_settlement_bool() is False:
            return False

        player_hand = self._resources
        for key in player_hand:
            if (key == "brick" or key == "wood") and player_hand[key] < 1:
                # if we are in the setup phase, do not require resources to build
                if len(self._roads) < 2:
                    return True
                return False

        # remove the resources for payment to build road
        for key in player_hand:
            if key == "brick" or key == "wood":
                resource_value = player_hand[key]
                player_hand[key] = resource_value - 1

        return True

    def robber_rolled(self, game, player):
        """
        If number 7 is rolled from the dice, the robber location needs to be moved and both the hex tiles at the old
        robber location and new robber location need to be updated
        Takes the GameBoard and Player objects as parameters
        """

        game.update_text_box(str(player.get_player_name()) + " Click on a tile to move the robber")

        # Loop to wait for player to select new robber location
        end_turn = False
        while end_turn is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #store coordinates of the player's mouse click
                    mouse_x, mouse_y = event.pos
                    # iterate through HexTile objects and find click closest to center of a hex tile
                    hex_tiles = game.get_hex_tiles()
                    for hex_tile in hex_tiles:
                        hex_tile_coords = hex_tile.get_center_coords()
                        hex_x, hex_y = hex_tile_coords[0], hex_tile_coords[1]
                        distance_x = hex_x - mouse_x
                        distance_y = hex_y - mouse_y
                        # Checking if the mouse click is within the center of the hex tile
                        if distance_x > -40 and distance_x < 40 and distance_y > -40 and distance_y < 40:
                            #game.update_robber_position(hex_tile_coords)
                            old_robber = game.get_robber_tile()
                            old_robber.set_robber(False)
                            game.set_robber_tile(hex_tile)
                            hex_tile.set_robber(True)
                            game.update_robber_position()
                            return

    def add_victory_point(self, number_of_points):
        """
        Takes an integer, number_of_points, as the parameter
        Updates the number of victory points a player has currently
        """
        self._victory_points += number_of_points