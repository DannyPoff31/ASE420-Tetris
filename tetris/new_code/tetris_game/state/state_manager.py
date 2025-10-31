"""
Author: Nate Brewer
Class to manage the states, their transitions, delegating updates etc.
"""

from state import States, Game, Pause, GameOver, Menu, Setting

class StateManager():
    def __init__(self, config, input, renderer):

        self.current_state_string = 'game' # Start at the menu state

        self.config = config
        self.input = input
        self.renderer = renderer

        # All available states will be labeled as a map
        self.states = {
            'pause': Pause(config=self.config, input=self.input, renderer=self.renderer),
            'game': Game(config=self.config, input=self.input, renderer=self.renderer),
            'gameover': GameOver(config=self.config, input=self.input, renderer=self.renderer),
            'menu': Menu(config=self.config, input=self.input, renderer=self.renderer),
            'setting': Setting(config=self.config, input=self.input, renderer=self.renderer)
        }

        self._change_state(self.current_state_string)


    def update(self, screen):
        # Todo: grab state and get an update 

        # Update state 
        self.current_state.update(screen)

    def _change_state(self, new_state_string):
        self.current_state = self.states[new_state_string]