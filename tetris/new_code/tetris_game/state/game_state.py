import pygame as pg
import sys
from state import States

from game.piece import Piece
from game.board import Board
from game.piece_action import PieceAction

from tetris.new_code.tetris_game.game.game_command import CommandFacotry


class Game(States):
    def __init(self, config, input, renderer):
        States.__init__(self, config, input, renderer)
        self.next = 'game'

        # Injected Dependencies
        self.config = config
        self.input = input
        self.renderer = renderer

        # State specific objects
        self.command_factory = CommandFacotry()

        # Board instantiation
        self.board_height = 20
        self.board_width = 10
        self.board = Board(self.board_height, self.board_width)

        # 
        self.pressing_down = False


    def cleanup(self):
        print("Cleaning up menu")
    def startup(self):
        print("starting menu")
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Game state keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,0,255))