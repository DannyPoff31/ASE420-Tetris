import pygame as pg # type: ignore (ignores the "could not resolve" error)
import sys
from .state import States

from ..game.piece import Piece
from ..game.board import Board
from ..game.piece_action import PieceAction

from ..game.game_command import CommandFacotry


class GameOver(States):
    def __init(self, config, input, renderer):
        States.__init__(self, config, input, renderer)
        self.next = 'menu'

        # Injected Dependencies
        self.config = config
        self.input = input
        self.renderer = renderer

        # Board instantiation
        self.board_height = 20
        self.board_width = 10
        self.board = Board(self.board_height, self.board_width)


        self.game_actions = {
            PieceAction.QUIT: quit_game,
            PieceAction.MENU: toggle_pause
        }

    def cleanup(self):
        print("Cleaning up menu")
    def startup(self):
        print("starting menu")
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Game state keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
            
    def update(self):
        
        # Gameover state   
        return False

        self.draw()
    def draw(self):
        print('Draw!')

    def toggle_pause():
        next = 'pause'
