import pygame

from game.board import Board
from game.piece import Piece
from game.piece_action import PieceAction

from ui.renderer import Renderer

from input.input import Input
from tetris.new_code.tetris_game.game.game_command import CommandFacotry

from state.state import States

from config.config import Config

def run_game():

    def quit_game():
        nonlocal running
        running = False
    
    def toggle_pause():
        nonlocal state
        state = "paused" if state == "state" else  "start"

    game_actions = {
        PieceAction.QUIT: quit_game,
        PieceAction.PAUSE: toggle_pause
    }

    # Begin the config process 
    config = Config()

    # Create the abstract state class to be handled throughout the loop
    state = States()

    # Start the pygame client
    pygame.init()
    screen = pygame.display.set_mode(config)
    pygame.display.set_caption("Code^3 Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans', 25, True, False)

    # What creates the screen
    renderer = Renderer(screen = screen)

    # Create input
    input_handler = Input(config)

    # Create command factory
    command_factory = CommandFacotry()

    pressing_down = False

    board_height = 20
    board_width = 10
    #Create new instance of board
    board = Board(board_height, board_width)

    #Default starting position for pieces
    piece_start_XPos = 3
    piece_start_YPos = 0
    piece = Piece(piece_start_XPos, piece_start_YPos)

    # Main run Bool
    running = True

    counter = 0

    # Main Run loop
    while running:

        counter += 1
        if counter > 100000:
            counter = 0

        # This is what checks what keys are being pressed
        actions = input_handler.get_actions()
        
        need_new_piece = False

        for action in actions:
            if action in game_actions:
                game_actions[action]()  
            else:
                command = command_factory.create_command(action)
                if command:
                    result = command.execute(piece, board)
                    # Check if hard drop was executed and we need a new piece
                    if result is True:
                        need_new_piece = True

        # Create new piece if needed (after hard drop)
        if need_new_piece and state == "start":
            piece = Piece(piece_start_XPos, piece_start_YPos)
            # Check for game over
            if board.intersects(piece):
                state = "gameover"

        # Check if down key is being held
        pressing_down = input_handler.is_down_pressed()

        # Check if we need to automatically go down
        # When holding down, move faster (every 5 frames instead of fps//2)
        should_move_down = False
        if pressing_down:
            should_move_down = counter % 5 == 0  # Move every 5 frames when holding down
        else:
            should_move_down = counter % (fps // 2) == 0  # Normal speed
            
        if should_move_down and not need_new_piece:

            if state == "start":

                old_y = piece.yShift

                piece.yShift += 1

                if board.intersects(piece):
                    piece.yShift = old_y
                    # Freeze the piece
                    board.freeze_piece(piece)
                    # Create a new piece
                    piece = Piece(piece_start_XPos, piece_start_YPos)
                    # Check for game over
                    if board.intersects(piece):
                        state = "gameover"
            else:
                running = False
            

        renderer.render_board(board)

        renderer.draw_piece(piece)

        # refresh the screen
        pygame.display.flip()
        clock.tick(fps)
    
    pygame.quit()

if __name__ == "__main__":
    run_game()