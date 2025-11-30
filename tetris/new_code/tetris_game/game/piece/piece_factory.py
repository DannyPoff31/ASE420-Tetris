"""
    Author: Nathaniel Brewer

    Will act as a factory for each type of registered pieces. Piece registry will happen when the user
    chooses the game type they would like to play
"""

from .abstract_piece import AbstractPiece
from .special_pieces.abstract_special import AbstractSpecialPiece

from .piece import Piece
from .special_pieces.rocket_piece import RocketPiece 

import random

class PieceFactory:

    # Registry for all current pieces in the game, makes dynamically creating the pieces easier

    _piece_reg = {
        'I': Piece,
        'Z': Piece,
        'S': Piece,
        'L': Piece,
        'J': Piece,
        'T': Piece,
        'O': Piece,
        'rocket': RocketPiece,
    } 

    def __init__(self, gamemode_config):
        self.gamemode_config = gamemode_config # a map that holds all the pieces the gamemode allows for

        # Pool for the factory to select from
        self.piece_pool = []

        if self.gamemode_config['mode'] == 'classic' or gamemode_config.get('include_classic', True):
            self.piece_pool.extend(['I', 'Z', 'S', 'L', 'J', 'T', 'O'])

        # Add the special pieces
        self.piece_pool.extend(gamemode_config.get('special_pieces', []))

    def create_random_piece(self, x, y):
        piece_type = random.choice(self.piece_pool)
        piece_class = self._piece_reg[piece_type]

        # For classic pieces, pass the piece_type so it knows which shape
        # For special pieces, they handle their own shape
        if piece_type in ['I', 'Z', 'S', 'L', 'J', 'T', 'O']:
            return piece_class(x, y, piece_type=piece_type)
        else:
            # Special pieces
            return piece_class(x, y)


        
