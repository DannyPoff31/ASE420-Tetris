from abc import ABC, abstractmethod

class AbstractGamemode(ABC):
    @abstractmethod
    def update(self, game_state):
        """Update the game logic for this mode."""
        pass

    @abstractmethod
    def calculate_score(self, lines_cleared):
        """Calculate the score based on the mode's rules."""
        pass