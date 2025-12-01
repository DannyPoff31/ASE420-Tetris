"""
Author: Nathaniel Brewer
Class to manage the states, their transitions, delegating updates etc.
"""

from .game_state import Game
from .gameover_state import GameOver
from .menu_state import Menu
from .setting_state import Setting
from .pause_state import Pause
from .gamemode_select_state import GamemodeSelection

class StateManager():
    def __init__(self, config, input, renderer):

        self.current_state_string = 'menu' # Start at the menu state

        self.config = config
        self.input = input
        self.renderer = renderer

        # Create game instance once and reuse it
        game_instance = Game(config=self.config, input=self.input, renderer=self.renderer)

        # All available states will be labeled as a map
        self.states = {
            'pause': Pause(config=self.config, input=self.input, renderer=self.renderer),
            'game': game_instance,
            'gamemode': GamemodeSelection(config=self.config, input=self.input,renderer=self.renderer),
            'gameover': GameOver(config=self.config, input=self.input, renderer=self.renderer),
            'menu': Menu(config=self.config, input=self.input, renderer=self.renderer),
            'settings': Setting(config=self.config, input=self.input, renderer=self.renderer),
            'restart': game_instance  # Use the same instance for restart
        }

        self.current_state = self.states[self.current_state_string]


    def update(self):
        # Todo: grab state and get an update 

        # Update state 
        result = self.current_state.update()

        if result == self.current_state_string:
            # Same state
            return True
        elif result is False or result == 'quit':
            # Game should end!
            return False
        
        # Change state
        self._change_state(result)

        # Check for game state

        
        # Always return true to continue game
        return True

    def _change_state(self, new_state_string):
        # Handle restart specially
        if new_state_string == 'restart':
            # Reset the game state
            self.states['game'].restart()
            new_state_string = 'game'
        
        # Change string
        self.current_state_string = new_state_string

        # Reset to pre-init state (cleanup old state)
        self.current_state.cleanup()

        # Change state
        self.current_state = self.states[new_state_string]
        

