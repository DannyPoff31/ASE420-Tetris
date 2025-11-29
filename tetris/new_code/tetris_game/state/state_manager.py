"""
Author: Nathaniel Brewer
Class to manage the states, their transitions, delegating updates etc.
"""

from .abstract_state import AbstractState
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

        # All available states will be labeled as a map
        self.states = {
            'pause': Pause(config=self.config, input=self.input, renderer=self.renderer),
            'game': Game(config=self.config, input=self.input, renderer=self.renderer),
            'gamemode': GamemodeSelection(config=self.config, input=self.input,renderer=self.renderer),
            'gameover': GameOver(config=self.config, input=self.input, renderer=self.renderer),
            'menu': Menu(config=self.config, input=self.input, renderer=self.renderer),
            'settings': Setting(config=self.config, input=self.input, renderer=self.renderer),
            'restart': Game(config=self.config, input=self.input, renderer=self.renderer)
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

        print(self.current_state_string)
        
        # Always return true
        return True

    def _change_state(self, new_state_string):
        # Change string
        self.current_state_string = new_state_string

        # Reset to pre-init state
        self.current_state.cleanup()

        # Change state
        self.current_state = self.states[new_state_string]

