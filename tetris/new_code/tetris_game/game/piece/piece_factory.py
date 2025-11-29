"""
    Author: Nathaniel Brewer

    Will act as a factory for each type of registered pieces. Piece registry will happen when the user
    chooses the game type they would like to play
"""

from .abstract_piece import AbstractPiece
from .special_pieces.abstract_special import AbstractSpecialPiece

import random

class PieceFactory:
    def __init__(self, piece_map):
        self.piece_map = piece_map # a map that holds all the pieces the gamemode allows for

    def create_random_piece(self, spawn_params):
        piece_type = random.choice(self.piece_map)
        
    def 