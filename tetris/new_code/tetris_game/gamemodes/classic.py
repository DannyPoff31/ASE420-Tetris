from .abstract_gamemode import AbstractGamemode

from ..game.board import Board

from ..game.game_command import CommandFacotry

class Classic(AbstractGamemode):
    def __init__(self, gamemode_config, config):
        super().__init__(gamemode_config)

        # State specific objects
        self.command_factory = CommandFacotry()

        self.config = config

        # Fast down
        self.pressing_down = False

        # Board instantiation
        self.board_height = 20
        self.board_width = 10

        # Default Starting position for pieces
        self.piece_start_xPos = (self.board_width - 4) // 2
        self.piece_start_yPos = 0

        self._start_up()

    def restart(self):
        self._start_up()

    def _start_up(self):
        self.board = Board(self.board_height, self.board_width)
        self.blocks_placed = 0
        self.points = 0

        # Create init piece
        self._create_pieces()

    def _create_pieces(self):
        self.piece = self.piece_factory.create_random_piece(self.piece_start_xPos, self.piece_start_yPos)
        self.next_piece = self.piece_factory.create_random_piece(self.piece_start_xPos, self.piece_start_yPos)
    
    def calculate_score(self, lines_cleared):
        self.points += self.SCORING[lines_cleared - 1]

    def handle_downkey(self, pressing_down, counter, fps):
        # Handle automatic downward movement
        should_move_down = False
        
        if pressing_down:
            should_move_down = counter % 5 == 0  # Move every 5 frames when holding down
        else:
            should_move_down = counter % (fps // 2) == 0  # Normal speed
        
        if should_move_down:
            # Try to move piece down
            self.piece.yShift += 1
            
            if self.board.intersects(self.piece):
                self.piece.yShift -= 1
                # Freeze and handle new piece creation
                result = self.board.freeze_piece(self.piece)
                
                # Special Block 

                lines_broken = result

                # Play click sound when block is placed
                self.config.play_click_sound()

                # Special block: create flame effect for cleared columns
                #if self.piece.is_special and cleared_columns:
                    #for col_x in cleared_columns:
                        #self.renderer.create_column_flame_effect(col_x, self.board_height)
                #else:
                    # Normal block: create particles for each cleared line
                    #for line_y in cleared_indices:
                        #self.renderer.create_line_clear_particles(line_y, self.board_width)
                
                if lines_broken > 0:
                    self.calculate_score(lines_broken)
                self.blocks_placed += 1

                # Create new piece
                self._create_pieces()

                # Check for game over with the new piece
                if self.board.intersects(self.piece):
                    return "gameover"

        return 'game'

    def update(self, action): 
        # Reset lines broken
        lines_broken = 0

        need_new_piece = False

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
                    self.config.play_click_sound()
                    # Create particles for each cleared line
                    #for line_y in cleared_indices:
                        #self.renderer.create_line_clear_particles(line_y, self.board_width)
                    if lines_broken > 0:
                        self.calculate_score(lines_broken)
                    self.blocks_placed += 1
                    need_new_piece = True

        if need_new_piece:
            # Create new piece (after hard drop)
            self._create_pieces()
            #self.renderer.trigger_screen_flash()

            # Check for game over with the new piece
            if self.board.intersects(self.piece):
                return "gameover"
        
        return 'game'