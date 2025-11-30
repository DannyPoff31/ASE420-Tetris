from abc import abstractmethod

from ..abstract_piece import AbstractPiece

class AbstractSpecialPiece(AbstractPiece):
    def __init__(self, x, y, piece_type=None, piece_color=None):
        super().__init__(x, y, piece_type, piece_color)

        self.is_special = True
        

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
    def instant_drop(self, board):
        pass

    @abstractmethod
    def get_figure(self):
        pass

    # Handle the special ability 
    @abstractmethod
    def special_ability(self, board):
        pass