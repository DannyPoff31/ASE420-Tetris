import pygame
from tetris.new_code.tetris_game.piece import Piece
from constants import BLACK, WHITE, GRAY

# This initalizes the board - will be called everytime the game starts
class Board:
    def __init__(self, height, width):
        self = self
        self.height = height
        self.width = width
        self.field = []
        self.state = "play" # state will be either play or pause (if we add a pause)
        self.blockPixelSize = 20 # Was Tzoom

        for i in range(self.height):
            new_line = [0] * self.width # polymorphism using * 
            self.field.append(new_line)

    def intersects(self, figures, xShift, yShift):
        intersection = False

        # WHAT IS 4??????
        # I is the height(Y)
        for i in range(4):
            # J is the width(X)
            for j in range(4):
                if i * 4 + j in figures:
                    if i + yShift > self.height - 1 or \
                       j + xShift > self.width - 1 or \
                       j + xShift < 0 or \
                       self.field[i + yShift][j + xShift] > 0:
                            self.state = "gameover"
                            #TODO: Make this game state do something
                            intersection = True
        return intersection
    
    # This will stop the piece from moving (called after it intersects with another piece)
    def freezePiece(self, figure, xShift, yShift):
        createNewPiece = False # Bool to tell game.py to create a new figure

        for i in range(4):
            for j in range(4):
                if i *4 + j in figure:
                    self.field[i + yShift][j + xShift] = 1
        self.breakLines()

        createNewPiece = True
        return createNewPiece
    
    def breakLines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            # this row is full
            if zeros == 0:
                lines += 1
                for k in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[k][j] = self.field[k - 1][j]

    def clearBoard(self):
        #TODO: Clear the board and it's un-needed attributes (states)
        return False