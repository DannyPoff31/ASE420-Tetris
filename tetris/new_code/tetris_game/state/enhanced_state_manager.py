"""
    Author: Nathaniel Brewer

    Extension of State manager. This will help with the pause state and the settings state
"""
from .state_manager import StateManager

class EnhancedStateManager(StateManager):
    def __init__(self, config, input, renderer):
        super().__init__(config, input, renderer)

        # should not cleanup this state when transitioning
        self.preserver_states = {'game'}

        self.resume_state = {'pause'}

        self.settings_state = {'settings'}

    def _change_state(self, new_state_string):
        should_cleanup = True

        # Pausing the game
        pause_resume = (self.current_state_string == 'game' and new_state_string == 'pause') or \
            (self.current_state_string =='pause' and new_state_string == 'game') or \
            (self.current_state_string =='settings')

        if pause_resume:
            should_cleanup = False

        if should_cleanup:
            self.current_state.cleanup()

        # Change state
        self.current_state_string = new_state_string
        self.current_state = self.states[new_state_string]

        # Call startup for pause state specifically, or for any state when doing cleanup
        if (new_state_string == 'pause') or (should_cleanup and hasattr(self.current_state, 'startup')):
            if hasattr(self.current_state, 'startup'):
                self.current_state.startup()
