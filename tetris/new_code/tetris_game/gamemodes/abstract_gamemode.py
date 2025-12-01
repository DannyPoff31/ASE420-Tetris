from abc import ABC, abstractmethod

from ..game.piece.piece_factory import PieceFactory

class AbstractGamemode(ABC):
    def __init__(self, gamemode_config, config):

        self.config = config

        self.piece_factory = PieceFactory(gamemode_config)

        self.SCORING = [
            40,     # Single Line 
            100,    # Double
            300,    # Triple
            1200    # Tetris (4-lines)
        ]


    @abstractmethod
    def update(self, game_state):
        # Update the game logic for this mode
        pass

    @abstractmethod
    def calculate_score(self, lines_cleared):
        # Calculate the score based on the mode's rules
        pass

    @abstractmethod
    def handle_downkey(self, pressing_down, counter, fps):
        # For the fast down key being pressed
        pass