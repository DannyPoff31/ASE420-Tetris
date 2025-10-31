import pygame as pg # type: ignore (ignores the "could not resolve" error)
import sys
from .state import States

from ..game.piece import Piece
from ..game.board import Board
from ..game.piece_action import PieceAction

from ..game.game_command import CommandFacotry


class Pause(States):
    def __init__(self, config, input, renderer):
        States.__init__(self, config, input, renderer)
        self.next = 'pause'

        # Injected Dependencies
        self.config = config
        self.input = input
        self.renderer = renderer

        # Fast down
        self.pressing_down = False


        self.game_actions = {
            PieceAction.QUIT: '',
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

        # Add menu to Resume/quit/settings 

        self.draw()
    def draw(self):
        print("draw")

    def toggle_pause():
        next = 'pause'