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

        self.gamemode = None
        self.startup()

    def cleanup(self):
        # Don't clear or reset when pausing - we want to preserve the game state
        pass

    def restart(self):
        # Force recreation of gamemode for restart
        self.startup()
        if self.gamemode is not None:
            self.gamemode.restart()

    # Used to restart the game by reseting vars (e.g. if the player wants to replay after losing)
    def startup(self): 

        self.drawn = False

        # If there's a pending gamemode, use it (overrides existing gamemode)
        if self.config.pending_gamemode is not None:
            self.gamemode = self.config.pending_gamemode
            # Clear pending_gamemode after using it
            self.config.pending_gamemode = None
        # Only create a new gamemode if we don't have one yet
        elif self.gamemode is None:
            # Create a default Classic gamemode if none was selected
            from ..gamemodes.classic import Classic
            default_config = {'mode': 'classic', 'special_pieces': [], 'include_classic': True}
            self.gamemode = Classic(default_config, self.config)
        
        # Start background music when game starts
        self.config.play_bgm()

    def update(self):
        gamestate = 'game'
        
        # get user input
        actions = self.input.get_actions()

        for action in actions:
            if action == PieceAction.QUIT:
                return 'quit'
            elif action in self.game_actions:
                return self.game_actions[action]


        pressing_down = self.input.is_down_pressed()
        if self.gamemode is not None:
            down_result = self.gamemode.handle_downkey(pressing_down, self.config.counter, self.config.fps)
            if down_result == "gameover":
                return "gameover"

        for action in actions:
            if action not in self.game_actions and action != PieceAction.QUIT:
                gamestate = self.gamemode.update(action)
                if gamestate == "gameover":
                    return "gameover"
        
        self.draw()
        return gamestate

    def draw(self):
        # Redraw the board and the piece
        self.renderer.render_board(self.gamemode.board)
        self.renderer.draw_piece(self.gamemode.piece)
        self.renderer.draw_score(self.gamemode.points)
        self.renderer.draw_level(self.gamemode.display_level)
        self.renderer.draw_next_piece(self.gamemode.next_piece)

        self.renderer.handle_vfx_pool(self.gamemode.vfx_pool)
        self.renderer.update_vfx()
        self.renderer.draw_vfx()
        self.gamemode.vfx_pool.clear()

    def toggle_pause():
        return 'pause'