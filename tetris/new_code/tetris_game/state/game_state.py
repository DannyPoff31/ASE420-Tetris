"""
    Author: Nathaniel Brewer

    This is the game state, this is where all the game logic will occur and any variables pertaining to the actual playing
    of tetris will occur.
"""

from .abstract_state import AbstractState

from ..game.piece.piece_action import PieceAction

class Game(AbstractState):
    def __init__(self, config, input, renderer):
        super().__init__(config, input, renderer)
        self.next = 'gameover'

        self.game_actions = {
            PieceAction.PAUSE: 'pause',
            PieceAction.QUIT: 'quit'
        }

        self.startup()

    def cleanup(self):
        # clear the screen
        self.renderer.clear()

        # Reset to pre-init values
        self.startup()

    def restart(self):
        self.startup()

        self.gamemode.restart()

    # Used to restart the game by reseting vars (e.g. if the player wants to replay after losing)
    def startup(self): 

        # Use pending gamemode or create a default Classic mode
        if self.config.pending_gamemode is not None:
            self.gamemode = self.config.pending_gamemode
        else:
            # Create a default Classic gamemode if none was selected
            from ..gamemodes.classic import Classic
            default_config = {'mode': 'classic', 'special_pieces': [], 'include_classic': True}
            self.gamemode = Classic(default_config, self.config)

        self.points = 0

    def update(self):

        gamestate = 'game'
        
        # get user input
        actions = self.input.get_actions()

        # Check if down key is being held
        pressing_down = self.input.is_down_pressed()

        for action in actions:

            if action in self.game_actions:
                # Activates the actions that are stored inside the 'game_actions' map
                return self.game_actions[action]  
            else:
                # Pass the action to the gamemode
                gamestate = self.gamemode.update(action)


        # Pass the pressing_down state to gamemode for automatic downward movement
        gamestate = self.gamemode.handle_downkey(pressing_down, self.config.counter, self.config.fps)   
        
        self.draw()
        return gamestate

    def draw(self):
        # Redraw the board and the piece
        self.renderer.render_board(self.gamemode.board)
        self.renderer.draw_piece(self.gamemode.piece)
        self.renderer.draw_score(self.gamemode.points)

    def toggle_pause():
        return 'pause'