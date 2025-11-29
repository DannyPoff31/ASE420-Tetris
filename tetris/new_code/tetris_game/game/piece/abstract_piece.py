"""
    Author: Nathaniel Brewer

    This is the abstract piece class, all the characteristics of the piece are handled here. The location of the piece while it is dropping is also managed here
"""
from abc import ABC, abstractmethod

from ...main.constants import FIGURES

class AbstractPiece(ABC):
    def __init__(self, x, y, piece_type=None, piece_color=None):
        self.xShift = x
        self.yShift = y
        self.rotation = 0   
        self.figures = FIGURES

    @abstractmethod
    def go_side(self, newXShift, board):
        pass
        
    @abstractmethod
    def rotate(self, board):
        pass

    @abstractmethod
    def go_down(self, board):
        pass

    @abstractmethod
    def insance_drop(self, board):
        pass

    @abstractmethod
    def get_figure(self):
        pass

    def _freeze(self, board):
        return board.freeze_piece(self)

    # When pressing instant drop key
    def instant_drop(self, board):
        while not board.intersects(self):
            self.yShift += 1 
        self.yShift -= 1
        result = board.freeze_piece(self)
        print(result)
        # Return tuple (lines_broken, cleared_indices)
        return result
