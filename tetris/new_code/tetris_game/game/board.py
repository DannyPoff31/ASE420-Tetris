"""
Author: Nathaniel Brewer
"""
import pygame # type: ignore
from ..main.constants import BLACK, WHITE, GRAY, SPECIAL_BLOCK_WIDTH, SPECIAL_BLOCK_HEIGHT

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

        # Special block handling
        if piece.is_special:
            # Check if special block
            for i in range(SPECIAL_BLOCK_HEIGHT):
                for j in range(SPECIAL_BLOCK_WIDTH):
                    board_y = i + piece.yShift
                    board_x = j + piece.xShift

                    if (board_y >= self.height or board_y < 0 or 
                        board_x >= self.width or board_x < 0):
                        intersection = True
                        break
                    
                    if board_y >= 0 and board_x >= 0 and board_y < self.height and board_x < self.width:
                        if self.field[board_y][board_x] > 0:
                            intersection = True
                            break
                
                if intersection:
                    break
            return intersection

        # Normal block
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

        if piece.is_special:
            for i in range(SPECIAL_BLOCK_HEIGHT):
                for j in range(SPECIAL_BLOCK_WIDTH):
                    board_y = i + piece.yShift
                    board_x = j + piece.xShift
                    
                    if (0 <= board_y < self.height and 0 <= board_x < self.width):
                        self.field[board_y][board_x] = -1  # Special marker
            
            self.process_special_block(piece.xShift, piece.yShift)

            return 0, []
        
        for i in range(4):
            for j in range(4):
                if i * 4 + j in piece.get_figure():
                    board_y = i + piece.yShift
                    board_x = j + piece.xShift

                    if (0 <= board_y < self.height and 0 <= board_x < self.width):
                        self.field[board_y][board_x] = piece.color

        broken_lines, cleared_indices = self.break_lines()
        
        return broken_lines, cleared_indices
    
    def process_special_block(self, start_x, start_y):
        """Process special block: fall down vertically and clear blocks in 3 columns"""
        for i in range(SPECIAL_BLOCK_HEIGHT):
            for j in range(SPECIAL_BLOCK_WIDTH):
                board_y = start_y + i
                board_x = start_x + j
                if (0 <= board_y < self.height and 0 <= board_x < self.width):
                    if self.field[board_y][board_x] == -1:
                        self.field[board_y][board_x] = 0
        
        # Special block falls down and clearing all blocks in 3 lines
        # Clear all blocks in the 3 columns from top to bottom (entire columns)
        for j in range(SPECIAL_BLOCK_WIDTH):
            col_x = start_x + j
            if 0 <= col_x < self.width:
                for i in range(self.height):
                    if self.field[i][col_x] > 0:
                        self.field[i][col_x] = 0
    
    def break_lines(self):
        lines = 0
        cleared_line_indices = []  # Store which lines were cleared
        i = self.height - 1  # Start from bottom
        while i >= 0:
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            
            # this row is full
            if zeros == 0:
                lines += 1
                cleared_line_indices.append(i)  # Record which line was cleared
                # Remove the full line by moving all rows above it down
                for k in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[k][j] = self.field[k - 1][j]
                # Clear the top row
                for j in range(self.width):
                    self.field[0][j] = 0
                # Don't increment i since we need to check this row again
                # (a new row has moved down to this position)
            else:
                i -= 1  # Only move up if no line was cleared

        return lines, cleared_line_indices

    def clear_board(self):
        #TODO: Clear the board and it's un-needed attributes (states)
        return False