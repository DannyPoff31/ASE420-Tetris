"""
    Author: Nathaniel Brewer

    Special Block gamemode where special blocks you have chosen are allowed to be placed
"""
from .abstract_gamemode import AbstractGamemode

from ..game.board import Board

from ..game.game_command import CommandFactory

class Special(AbstractGamemode):
    def __init__(self, gamemode_config, config):
        super().__init__(gamemode_config, config)

        # State specific objects
        self.command_factory = CommandFactory()

        # All VFX commands will be accessed here from the 
        self.vfx_pool = []

        # Fast down
        self.pressing_down = False

        # Track when piece last moved down to help with the level incrementation
        self.last_move_counter = 0

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
        self.piece = None

         # Reset lines to 0
        self.total_lines_broken = 0

        # Set game level to starting
        self.config.level = 1
        self.display_level = 1

        self.board = Board(self.board_height, self.board_width)
        self.blocks_placed = 0
        self.points = 0

        # Create init piece
        self._create_pieces()

    def _create_pieces(self):
        # new game will need a init piece to begin and then will create next piece
            
        if self.piece == None:
            self.piece = self.piece_factory.create_random_piece(self.piece_start_xPos, self.piece_start_yPos)

            # Prevent special pieces from being first

            while self.piece.is_special:
                self.piece = self.piece_factory.create_random_piece(self.piece_start_xPos, self.piece_start_yPos)

        else:
            self.piece = self.next_piece

        self.next_piece = self.piece_factory.create_random_piece(self.piece_start_xPos, self.piece_start_yPos)

    def calculate_score(self, lines_cleared):
        
        # No points for special pieces
        if(self.piece.is_special):
            return

        self.points += self.SCORING[lines_cleared - 1]

    def handle_downkey(self, pressing_down, counter, fps): 
        # Handle automatic downward movement
        should_move_down = False
        
        if pressing_down:
            should_move_down = (self.config.counter - self.last_move_counter) >= 5   # Move every 5 frames when holding down
        else:
            should_move_down = (self.config.counter - self.last_move_counter) >= (self.config.fps // 2) # Normal speed
        
        if should_move_down:
            # Try to move piece down
            self.piece.yShift += 1
            self.last_move_counter = self.config.counter
            
            if self.board.intersects(self.piece):
                self.piece.yShift -= 1

                if self.piece.is_special:
                    # Play click sound when special block lands
                    self.config.play_click_sound()
                    
                    # Execute special ability (clears columns)
                    self.piece.special_ability(self.board)
                    
                    # Create flame effects for the cleared columns
                    for j in range(self.piece.width):
                        col_x = self.piece.xShift + j
                        if 0 <= col_x < self.board_width:
                            self.vfx_pool.append({
                                'type': 'column_flame',
                                'column_x': col_x,
                                'board_height': self.board_height
                            })
                    
                    self.blocks_placed += 1
                else:
                    # Freeze and handle new piece creation
                    result = self.board.freeze_piece(self.piece)
                    lines_broken, cleared_indices = result

                    # Play click sound when block is placed
                    self.config.play_click_sound()

                    # Create particles for each cleared line
                    for line_y in cleared_indices:
                        self.vfx_pool.append({
                            'type': 'line_clear',
                            'line_y': line_y,
                            'board_width': self.board_width
                        })  
                    
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
                if self.piece.is_special:
                    # Special piece hard drop
                    self.config.play_click_sound()
                    
                    # Create flame effects for the cleared columns
                    for j in range(self.piece.width):
                        col_x = self.piece.xShift + j
                        if 0 <= col_x < self.board_width:
                            self.vfx_pool.append({
                                'type': 'column_flame',
                                'column_x': col_x,
                                'board_height': self.board_height
                            })
                    
                    self.blocks_placed += 1
                    need_new_piece = True
                else:
                    # Normal piece hard drop
                    lines_broken, cleared_indices = result
                    
                    self.total_lines_broken += lines_broken

                    # Play click sound when block is placed (hard drop)
                    self.config.play_click_sound()
                    
                    # Create particles for each cleared line
                    for line_y in cleared_indices:
                        self.vfx_pool.append({
                            'type': 'line_clear',
                            'line_y': line_y,
                            'board_width': self.board_width
                        })
                    if lines_broken > 0:
                        self.calculate_score(lines_broken)
                    self.blocks_placed += 1
                    need_new_piece = True

        if need_new_piece:
            # Create new piece (after hard drop)
            self._create_pieces()

            # Check for game over with the new piece
            if self.board.intersects(self.piece):
                return "gameover"
        
        # Check level requirements (every 10 blocks broken level += 1)
        if((self.total_lines_broken / self.config.level) // 10):
            self.config.level += 0.25
            self.display_level += 1

        return 'game'

        