import pygame # type: ignore
from ..main.constants import BLACK, WHITE, GRAY

# This initalizes the board - will be called everytime the game starts
class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.state = "play" # state will be either play or pause (if we add a pause)
        self.blockPixelSize = 20 # Was Tzoom

        for i in range(self.height):
            new_line = [0] * self.width # polymorphism using * 
            self.field.append(new_line)

    def intersects(self, piece):
        intersection = False

        # Check each block of the 4x4 piece grid
        # I is the height(Y)
        for i in range(4):
            # J is the width(X)
            for j in range(4):
                if i * 4 + j in piece.get_figure():
                    # Calculate the actual board position
                    board_y = i + piece.yShift
                    board_x = j + piece.xShift
                    
                    # Check bounds first to avoid index errors
                    if (board_y >= self.height or board_y < 0 or 
                        board_x >= self.width or board_x < 0):
                        intersection = True
                        break
                    
                    # Check if there's already a piece at this position
                    if self.field[board_y][board_x] > 0:
                        intersection = True
                        break
            
            if intersection:
                break
                
        return intersection
    
    # This will stop the piece from moving (called after it intersects with another piece)
    def freeze_piece(self, piece):
        createNewPiece = False # Bool to tell game.py to create a new figure

        for i in range(4):
            for j in range(4):
                if i * 4 + j in piece.get_figure():
                    board_y = i + piece.yShift
                    board_x = j + piece.xShift

                    if (0 <= board_y < self.height and 0 <= board_x < self.width):
                        self.field[board_y][board_x] = piece.color

        self.break_lines()
        createNewPiece = True
        return createNewPiece
    
    def break_lines(self):
        lines = 0
        i = self.height - 1  # Start from bottom
        while i >= 1:
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            # this row is full
            if zeros == 0:
                lines += 1
                # Remove the full line by moving all rows above it down
                for k in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[k][j] = self.field[k - 1][j]
                # Clear the top row
                for j in range(self.width):
                    self.field[1][j] = 0
                # Don't increment i since we need to check this row again
                # (a new row has moved down to this position)
            else:
                i -= 1  # Only move up if no line was cleared

    def clear_board(self):
        #TODO: Clear the board and it's un-needed attributes (states)
        return False