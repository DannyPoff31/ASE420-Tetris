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