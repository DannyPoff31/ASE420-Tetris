import pygame
import random

# Board Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Changed to immutable list
Colors = (
    (0, 0, 0),          # Black 
    (120, 37, 179),     # Purple
    (100, 179, 179),    # Cyan
    (80, 34, 22),       # Brown
    (80, 134, 22),      # Green
    (180, 34, 22),      # Red
    (180, 34, 122),     # Magenta
)

# Changed to immutable, can add figures later
# Each list for each figure is their rotation value.

# This is what gets ca
class Piece:
    def __init__(self, x, y):
        self = self
        self.xShift = x
        self.yShift = y
        self.rotation = 0
        # Changed to immutable, can add figures later
        # Each list for each figure is their rotation value.    
        self.figures = (
            [[1, 5, 9, 13], [4, 5, 6, 7]],  # I piece
            [[4, 5, 9, 10], [2, 6, 5, 9]],  # Z Piece
            [[6, 7, 9, 10], [1, 5, 6, 10]], # S Piece
            [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],      # L Piece
            [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],    # J Piece   
            [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],       # T Piece
            [[1, 2, 5, 6]], # O (square) piece
        )
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(Colors) - 1)

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