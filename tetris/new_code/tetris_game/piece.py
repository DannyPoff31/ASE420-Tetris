import pygame
import random
from constants import COLORS, FIGURES
from piece_action import PieceAction

class Piece:
    def __init__(self, x, y):
        self = self
        self.xShift = x
        self.yShift = y
        self.rotation = 0   
        self.figures = FIGURES
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(COLORS) - 1)

    # this gets called automatically - will get called faster when the down button is pressed
    def go_down(self, board):
        while not board.intersects(
            self.figures[self.type][self.rotation], 
            self.xShift, 
            self.yShift
        ):
            self.yShift += 1
        self.yShift -= 1
        board.freezePiece(self.figures[self.type][self.rotation], self.xShift, self.yShift)

    # When pressing left or right, move x amount
    def go_side(self, newXShift, board):
        old_x = self.xShift
        self.xShift += newXShift
        if board.intersects(
            self.figures[self.type][self.rotation],
            self.xShift,
            self.yShift
        ):
            self.xShift = old_x

    # When pressing instant drop key
    def instant_drop(self, board):
        while not board.intersects(
            self.figures[self.type][self.rotation], 
            self.xShift, 
            self.yShift
        ):
            self.yShift += 1 
        self.yShift -= 1
        board.freezePiece(self.figures[self.type][self.rotation], self.xShift, self.yShift)

    def rotate(self, board):
        def rotate_figure():
            self.rotation = (self.rotation + 1) % len(self.figures[self.type])

        oldRotation = self.rotation
        rotate_figure()
        if board.intersects(
            self.figures[self.type][self.rotation],
            self.xShift,
            self.yShift
        ):
            self.rotation = oldRotation

    def getFigure(self):
        return self.figures[self.type][self.rotation]