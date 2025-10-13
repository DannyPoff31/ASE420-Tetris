from abc import ABC, abstractmethod

class Command:

    @abstractmethod
    def execute(self):
        pass


class MoveCommand(Command):     
    def __init__(self, direction, distance=1):  # distance, in case we want to add extra ability
        super().__init__()
        self.direction = direction
        self.distance = distance # -1 for left +1 for right
    
    def execute(self, piece, board):
        self.piece = piece
        self.board = board

        piece.go_side(self.direction * self.distance, self.board)

class RotateCommand(Command):
    def __init__(self, clockwise=True):
        super().__init__()
        self.clockwise = clockwise

    def execute(self, piece, board):
        self.piece = piece
        self.board = board

        #Store old rotation
        old_rotation = piece.rotation
        if self.clockwise:
            piece.rotation = (piece.rotation + 1) % len(piece.figures[piece.type])
        else:
            piece.rotation = (piece.rotation - 1) % len(piece.figures[piece.type])

        can_rotate = not board.intersects(piece.getFigure(), piece.xShift, piece.yShift)
        piece.rotation = old_rotation
        
        #Success
        if can_rotate:
            piece.rotate(board)

        #Todo: something when failed
    
class SoftDropCommand(Command):
    def execute(self, piece, board):
        if not board.intersects(piece.getFigure(), piece.xShift, piece.yShift + 1):
            piece.yShift += 1
            return True
        return False
    
class HardDropCommand(Command):
    def execute(self, piece, board):
        piece.instant_drop(board)
        return True
    
# Creates a command map based on the enum commands listed in piece_action.py
class CommandFacotry:
    def __init__(self):
        
        from piece_action import PieceAction

        self._command_map = {
            PieceAction.MOVE_LEFT: lambda: MoveCommand(-1),
            PieceAction.MOVE_RIGHT: lambda: MoveCommand(+1),
            PieceAction.ROTATE_CLOCKWISE: lambda: RotateCommand(True),
            PieceAction.ROTATE_COUNTERCLOCKWISE: lambda: RotateCommand(False),
            PieceAction.SOFT_DROP: lambda: SoftDropCommand(),
            PieceAction.HARD_DROP: lambda: HardDropCommand()
        }

    # Gets a PieceAction enum passed by the input handler which then tells the piece what to do
    def create_command(self, action):
        command_constructor = self._command_map.get(action)
        return command_constructor() if command_constructor else None
