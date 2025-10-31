"""
Author: Nate Brewer
This is the game state, this is where all the game logic will occur and any variables pertaining to the actual playing
of tetris will occur.
"""

import pygame as pg # type: ignore (ignores the "could not resolve" error)
import sys
from state import States

from game.piece import Piece
from game.board import Board
from game.piece_action import PieceAction

from tetris.new_code.tetris_game.game.game_command import CommandFacotry


class Game(States):
    def __init(self, config, input, renderer):
        States.__init__(self, config, input, renderer)
        self.next = 'gameover'

        # Injected Dependencies
        self.config = config
        self.renderer = renderer
        self.input = input

        # State specific objects
        self.command_factory = CommandFacotry()

        # Board instantiation
        self.board_height = 20
        self.board_width = 10
        self.board = Board(self.board_height, self.board_width)

        # Fast down
        self.pressing_down = False

        self.game_actions = {
            PieceAction.PUASE: 'pause'
        }


        # Default Starting position for pieces
        self.piece_start_xPos = 3
        self.piece_start_yPos = 0
        self.piece = Piece(self.piece_start_xPos, self.piece_start_yPos)

    def cleanup(self):
        print("Cleaning up menu")

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

    def update(self):
        # Key Checker 
        actions = self.input.get_actions()

        need_new_piece = False

        # Determines which actions are happening 
        for action in actions:
            if action in self.game_actions:
                self.game_actions[action]()  
            else:
                command = self.command_factory.create_command(action)
                if command:
                    result = command.execute(self.piece, self.board)
                    if result is True:
                    # Hard drop was executed and we need a new piece
                        need_new_piece = True

        if need_new_piece:
        # Create new piece (after hard drop)
            piece = Piece(self.piece_start_XPos, self.piece_start_YPos)
            if self.board.intersects(piece):
                return "gameover"
            
        # Check if down key is being held
        pressing_down = self.input.is_down_pressed()

        # Check if we need to automatically go down
        # When holding down, move faster (every 5 frames instead of fps//2)
        should_move_down = False
        if pressing_down:
            should_move_down = self.config.counter % 5 == 0  # Move every 5 frames when holding down
        else:
            should_move_down = self.config.counter % (self.config.fps // 2) == 0  # Normal speed
            
        if should_move_down and not need_new_piece:

            old_y = piece.yShift

            piece.yShift += 1

            if self.board.intersects(piece):
                piece.yShift = old_y
                # Freeze the piece
                self.board.freeze_piece(piece)
                # Create a new piece
                piece = Piece(self.piece_start_XPos, self.piece_start_YPos)
                # Check for game over
                if self.board.intersects(piece):
                    return "gameover"
        
        self.draw()

    def draw(self):
        # Redraw the board and the piece
        self.renderer.render_board(self.board)
        self.draw_piece(self.piece)

    def toggle_pause():
        return 'pause'