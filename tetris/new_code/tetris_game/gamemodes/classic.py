from .abstract_gamemode import AbstractGamemode

from ..game.board import Board

class Classic(AbstractGamemode):
    def __init__(self, factory):
        super.__init__(self, factory)

        # Board instantiation
        self.board_height = 20
        self.board_width = 10
        self.board = Board(self.board_height, self.board_width)

        # Store the used piece types in a map to pass to the factory
        self.PIECE_TYPE = [Piece]  
        self.piece_factory = P
        

    def update(self, actions): 
