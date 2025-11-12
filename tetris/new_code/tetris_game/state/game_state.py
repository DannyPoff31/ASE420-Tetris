"""
Author: Nathaniel Brewer

This is the game state, this is where all the game logic will occur and any variables pertaining to the actual playing
of tetris will occur.
"""

import pygame as pg # type: ignore (ignores the "could not resolve" error)
import sys
from .state import States

from ..game.piece import Piece
from ..game.board import Board
from ..game.piece_action import PieceAction

from ..game.game_command import CommandFacotry

class Game(States):
    def __init__(self, config, input, renderer):
        States.__init__(self, config, input, renderer)
        self.next = 'gameover'

        # Injected Dependencies
        self.config = config
        self.renderer = renderer
        self.input = input

        self.game_actions = {
            PieceAction.PAUSE: 'pause'
        }

        self.points_per_line = [
            40,     # Single Line 
            100,    # Double
            300,    # Triple
            1200    # Tetris (4-lines)
        ]

        self.startup()

    def cleanup(self):
        # clear the screen
        self.renderer.clear()

        # Reset to pre-init values
        self.startup()

    # Used to restart the game by reseting vars (e.g. if the player wants to replay after losing)
    def startup(self):

        # State specific objects
        self.command_factory = CommandFacotry()

        # Board instantiation
        self.board_height = 20
        self.board_width = 10
        self.board = Board(self.board_height, self.board_width)

        # Fast down
        self.pressing_down = False

        # Default Starting position for pieces
        self.piece_start_xPos = 3
        self.piece_start_yPos = 0
        self.piece = Piece(self.piece_start_xPos, self.piece_start_yPos)

        self.points = 0

    def calculate_points(self, lines_broken):
        self.points += self.points_per_line[lines_broken - 1]
    

    def update(self):
        # Reset lines broken
        lines_broken = 0

        # Key Checker 
        actions = self.input.get_actions()

        need_new_piece = False

        # Determines which actions are happening 
        for action in actions:
            if action == PieceAction.QUIT:
                return 'quit'
            elif action in self.game_actions:
                # Activates the actions that are stored inside the 'game_actions' map
                return self.game_actions[action]  
            else:
                command = self.command_factory.create_command(action)
                if command:
                    result = command.execute(self.piece, self.board)
                    if result is not None and result is not False:
                        # Hard drop was executed - result is lines_broken
                        lines_broken = result
                        if lines_broken > 0:
                            self.calculate_points(lines_broken)
                        need_new_piece = True

        if need_new_piece:
        # Create new piece (after hard drop)
            self.piece = Piece(self.piece_start_xPos, self.piece_start_yPos)
            if self.board.intersects(self.piece):
                return "gameover"
            
        # Check if down key is being held
        pressing_down = self.input.is_down_pressed()

        # Check if we need to automatically go down
        # When holding down, move faster (every 5 frames instead of fps//2)
        should_move_down = False
        if pressing_down:
            should_move_down = self.config.counter % 5  # Move every 5 frames when holding down
        else:
            should_move_down = self.config.counter % (self.config.fps // 2) == 0  # Normal speed
            
        if should_move_down and not need_new_piece:

            old_y = self.piece.yShift

            self.piece.yShift += 1

            if self.board.intersects(self.piece):
                self.piece.yShift = old_y
                # Freeze the piece
                lines_broken = self.board.freeze_piece(self.piece)
                if lines_broken > 0:
                    self.calculate_points(lines_broken)
                # Create a new piece
                self.piece = Piece(self.piece_start_xPos, self.piece_start_yPos)
                # Check for game over
                if self.board.intersects(self.piece):
                    return "gameover"
        
        self.draw()
        return 'game'

    def draw(self):
        # Redraw the board and the piece
        self.renderer.render_board(self.board)
        self.renderer.draw_piece(self.piece)
        self.renderer.draw_score(self.points)

    def toggle_pause():
        return 'pause'