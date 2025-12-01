from .abstract_gamemode import Gamemode

class GamemodeManager:
    def __init__(self, initial_mode: Gamemode):
        self.current_mode = initial_mode

    def set_mode(self, new_mode: Gamemode):
        """Switch to a new gamemode."""
        self.current_mode = new_mode

    def update(self, game_state):
        """Delegate the update logic to the current gamemode."""
        self.current_mode.update(game_state)

    def calculate_score(self, lines_cleared):
        """Delegate score calculation to the current gamemode."""
        return self.current_mode.calculate_score(lines_cleared)