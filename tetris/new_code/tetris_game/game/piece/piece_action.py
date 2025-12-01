from enum import Enum

class PieceAction(Enum):
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    ROTATE_CLOCKWISE = "rotate_clockwise"
    ROTATE_COUNTERCLOCKWISE = "rotate_counterclockwise"
    SOFT_DROP = "soft_drop"
    HARD_DROP = "hard_drop"
    QUIT = "quit"
    PAUSE = "pause"
