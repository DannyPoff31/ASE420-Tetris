from abc import ABC, abstractmethod

class AbstractGamemode(ABC):
    def __init__(self, factory):

        self.SCORING = [
            40,     # Single Line 
            100,    # Double
            300,    # Triple
            1200    # Tetris (4-lines)
        ]


    @abstractmethod
    def update(self, game_state):
        """Update the game logic for this mode."""
        pass

    @abstractmethod
    def calculate_score(self, lines_cleared):
        """Calculate the score based on the mode's rules."""
        pass