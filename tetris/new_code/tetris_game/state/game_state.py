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

    def update(self):

        gamestate = 'game'
        
        # get user input
        actions = self.input.get_actions()

        need_new_piece = False

        # Determines which actions are happening 
        for action in actions:
            if action == PieceAction.QUIT:
                return 'quit'
            elif action in self.game_actions:
                # Activates the actions that are stored inside the 'game_actions' map
                return self.game_actions[action]  
            else:
                command = self.command_factory.create_command(action)
                if command:
                    result = command.execute(self.piece, self.board)
                    if result is not None and result is not False:
                        # Hard drop was executed - result is (lines_broken, cleared_indices)
                        if isinstance(result, tuple):
                            lines_broken, cleared_indices = result
                        else:
                            lines_broken = result
                            cleared_indices = []
                        # Play click sound when block is placed (hard drop)
                        self.renderer.play_click_sound()
                        # Create particles for each cleared line
                        for line_y in cleared_indices:
                            self.renderer.create_line_clear_particles(line_y, self.board_width)
                        if lines_broken > 0:
                            self._calculate_points(lines_broken)
                        self.blocks_placed += 1
                        need_new_piece = True

        if need_new_piece:
        # Create new piece (after hard drop)
            # Check if it's time for special block
            if self.blocks_placed % SPECIAL_BLOCK_INTERVAL == 0:
                # Spawn special block (3x6, centered)
                special_x = (self.board_width - SPECIAL_BLOCK_WIDTH) // 2
                self.piece = Piece(special_x, self.piece_start_yPos, is_special=True)
                self.next_piece = Piece(self.piece_start_xPos, self.piece_start_yPos)
                # Trigger screen flash effect
                self.renderer.trigger_screen_flash()
            else:
                self.piece = Piece(self.piece_start_xPos, self.piece_start_yPos, 
                                  self.next_piece.type, self.next_piece.color)
                self.next_piece = Piece(self.piece_start_xPos, self.piece_start_yPos)
            
            if self.board.intersects(self.piece):
                return "gameover"
            
        # Check if down key is being held
        pressing_down = self.input.is_down_pressed()

        for action in actions:

            if action in self.game_actions:
                # Activates the actions that are stored inside the 'game_actions' map
                return self.game_actions[action]  
            else:
                # Pass the action to the gamemode
                gamestate = self.gamemode.update(action)


            if self.board.intersects(self.piece):
                self.piece.yShift = old_y
                # Freeze the piece
                result = self.board.freeze_piece(self.piece)
                if isinstance(result, tuple) and len(result) == 3:
                    lines_broken, cleared_indices, cleared_columns = result
                elif isinstance(result, tuple) and len(result) == 2:
                    lines_broken, cleared_indices = result
                    cleared_columns = []
                else:
                    lines_broken = result
                    cleared_indices = []
                    cleared_columns = []
                
                # Play click sound when block is placed
                self.renderer.play_click_sound()
                
                # Special block: create flame effect for cleared columns
                if self.piece.is_special and cleared_columns:
                    for col_x in cleared_columns:
                        self.renderer.create_column_flame_effect(col_x, self.board_height)
                else:
                    # Normal block: create particles for each cleared line
                    for line_y in cleared_indices:
                        self.renderer.create_line_clear_particles(line_y, self.board_width)
                
                if lines_broken > 0:
                    self._calculate_points(lines_broken)
                self.blocks_placed += 1
                
                if self.blocks_placed % SPECIAL_BLOCK_INTERVAL == 0:
                    # Spawn special block
                    special_x = (self.board_width - SPECIAL_BLOCK_WIDTH) // 2
                    self.piece = Piece(special_x, self.piece_start_yPos, is_special=True)
                    self.next_piece = Piece(self.piece_start_xPos, self.piece_start_yPos)
                    # Trigger screen flash effect
                    self.renderer.trigger_screen_flash()
                else:
                    self.piece = Piece(self.piece_start_xPos, self.piece_start_yPos, 
                                      self.next_piece.type, self.next_piece.color)
                    self.next_piece = Piece(self.piece_start_xPos, self.piece_start_yPos)
                
                # Check for game over
                if self.board.intersects(self.piece):
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