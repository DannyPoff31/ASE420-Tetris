"""
    Author: Nathaniel Brewer

    This is the piece class, all the characteristics of the piece are handled here. The location of the piece while it is dropping is also managed here
"""

import random
from ...main.constants import COLORS, FIGURES

from ..piece.abstract_piece import AbstractPiece

class Piece(AbstractPiece):
    def __init__(self, x, y, piece_type=None, piece_color=None):
        self.xShift = x
        self.yShift = y
        self.rotation = 0   
        self.figures = FIGURES

        if piece_type is None:
             self.type = random.randint(0, len(self.figures) - 1)
        else:
            self.type = piece_type

        if piece_color is None:
            self.color = random.randint(1, len(COLORS) - 1)
        else:
            self.color = piece_color

    # When pressing left or right, move x amount
    def go_side(self, newXShift, board):
        
        old_x = self.xShift
        self.xShift += newXShift
        if board.intersects(self):
            self.xShift = old_x

    # When pressing instant drop key
    def instant_drop(self, board):
        while not board.intersects(self):
            self.yShift += 1 
        self.yShift -= 1
        result = self._freeze(board)
        # Return tuple (lines_broken, cleared_indices)
        return result

    def rotate(self, board):   
        def rotate_figure():
            self.rotation = (self.rotation + 1) % len(self.figures[self.type])

        oldRotation = self.rotation
        rotate_figure()
        if board.intersects(self):
            self.rotation = oldRotation

    # this gets called automatically - will get called faster when the down button is pressed
    def go_down(self, board):
        while not board.intersects(
            self.figures[self.type][self.rotation], 
            self.xShift, 
            self.yShift
        ):
            self.yShift += 1
        self.yShift -= 1
        return self._freeze(board)

    def get_figure(self):
        return self.figures[self.type][self.rotation]
