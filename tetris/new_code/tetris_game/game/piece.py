import pygame # type: ignore
import random
from ..main.constants import COLORS, FIGURES
from .piece_action import PieceAction

class Piece:
    def __init__(self, x, y, piece_type=None, piece_color=None, is_special=False):
        self = self
        self.xShift = x
        self.yShift = y
        self.rotation = 0   
        self.figures = FIGURES
        self.is_special = is_special

        if is_special:
            self.type = -1
            self.color = -1
        else:
            if piece_type is None:
                self.type = random.randint(0, len(self.figures) - 1)
            else:
                self.type = piece_type
            if piece_color is None:
                self.color = random.randint(1, len(COLORS) - 1)
            else:
                self.color = piece_color

    # this gets called automatically - will get called faster when the down button is pressed
    def go_down(self, board):
        if self.is_special:
            while not board.intersects(self):
                self.yShift += 1
            self.yShift -= 1
            return board.freeze_piece(self)
        
        while not board.intersects(
            self.figures[self.type][self.rotation], 
            self.xShift, 
            self.yShift
        ):
            self.yShift += 1
        self.yShift -= 1
        return board.freeze_piece(self)

    # When pressing left or right, move x amount
    def go_side(self, newXShift, board):
        if self.is_special:
            old_x = self.xShift
            self.xShift += newXShift
            from ..main.constants import SPECIAL_BLOCK_WIDTH
            if (self.xShift < 0 or self.xShift + SPECIAL_BLOCK_WIDTH > board.width or board.intersects(self)):
                self.xShift = old_x
            return
        
        old_x = self.xShift
        self.xShift += newXShift
        if board.intersects(self):
            self.xShift = old_x

    # When pressing instant drop key
    def instant_drop(self, board):
        while not board.intersects(self):
            self.yShift += 1 
        self.yShift -= 1
        result = board.freeze_piece(self)
        # Return tuple (lines_broken, cleared_indices)
        return result

    def rotate(self, board):
        # Special blocks cannot rotate
        if self.is_special:
            return
        
        def rotate_figure():
            self.rotation = (self.rotation + 1) % len(self.figures[self.type])

        oldRotation = self.rotation
        rotate_figure()
        if board.intersects(self):
            self.rotation = oldRotation

    def get_figure(self):
        if self.is_special:
            return []
        return self.figures[self.type][self.rotation]