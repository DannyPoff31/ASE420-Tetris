from .abstract_special import AbstractSpecialPiece

class RocketPiece(AbstractSpecialPiece):
    def __init__(self, x, y, piece_type=None, piece_color=None):
        super().__init__(x, y, piece_type, piece_color)

        self.type = -1
        self.color = -1

        self.width = 3
        self.height = 6

        # How often this block spawns, every X block is this block
        self.interval = 15
    
    # When pressing left or right, move x amount
    def go_side(self, newXShift, board):
        old_x = self.xShift
        self.xShift += newXShift
        if (self.xShift < 0 or self.xShift + self.width > board.width or board.intersects(self)):
            self.xShift = old_x
        return
        
    def rotate(self, board):
        # Cannot rotate
        return
    
        # this gets called automatically - will get called faster when the down button is pressed
    def go_down(self, board):
        while not board.intersects(self):
            self.yShift += 1
        self.yShift -= 1
        return self._freeze(board)
    
        # When pressing instant drop key
    def instant_drop(self, board):
        # Drop to the bottom
        while not board.intersects(self):
            self.yShift += 1 
        self.yShift -= 1
        
        # Execute special ability (clear columns)
        self.special_ability(board)
        
        # Return (0, []) since special pieces don't clear lines traditionally
        return (0, [])
    
    def get_figure(self):
        # Return blocks that represent the bottom of the 3-wide rocket for collision detection
        # Rocket is 6 blocks tall (0-5), so we want collision at the bottom (row 5)
        # But since we're in a 4x4 grid system, we use row 3 and adjust yShift
        # This creates invisible collision blocks 5 rows down from yShift
        return [12, 13, 14]  # Bottom row: positions (3,0), (3,1), (3,2)
    
    def special_ability(self, board):
        # Rocket clears all blocks in the 3 columns where it lands
        # Clear entire columns from top to bottom
        for j in range(self.width):  # Rocket is 3 blocks wide
            col_x = self.xShift + j
            if 0 <= col_x < board.width:
                # Clear entire column
                for i in range(board.height):
                    if board.field[i][col_x] > 0:
                        board.field[i][col_x] = 0