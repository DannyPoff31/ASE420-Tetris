import pygame

from board import Board
from tetris.new_code.tetris_game.ui.renderer import Renderer
from tetris.new_code.tetris_game.piece import Piece
from tetris.new_code.tetris_game.input.input import Input

from config import Config

def run_game():

    # Begin the config process 
    config = Config()

    size = [config.get_graphics_setting('window_width'), Config.get_graphics_setting('window_height')]
    fps = config.get_graphics_setting('fps')

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Code^3 Tetris")
    clock = pygame.time.Clock()

    # What creates the screen
    renderer = Renderer(screen = screen)

    #change to menu/settings/etc
    state = "start"

    running = True  # Main run Bool

    # Create input
    input_handler = Input(config)

    counter = 0
    pressing_down = False

    board_height = 20
    board_width = 10

    #Create new instance of board
    board = Board(board_height, board_width)

    font = pygame.font.SysFont('Comic Sans', 25, True, False)

    #Default starting position for pieces
    piece_start_XPos = 3
    piece_start_YPos = 0
    piece = Piece(piece_start_XPos, piece_start_YPos)

    while running:

        counter += 1
        if counter > 100000:
            counter = 0

        # This is what checks what keys are being pressed
        # Returns True if key is pressed down, false otherwise
        # TODO: Might be a better way to do this?
        commands = input_handler.get_actions(piece, board)

        for command in commands:
            if command:
                command.execute(piece, board)

        # Check if we need to automatically go down
        if counter % (fps // 2) == 0 or pressing_down:
            if state == "start":
                if not board.intersects(piece.getFigure(), piece.xShift, piece.yShift + 1):
                    piece.yShift += 1
                else:
                    # Freeze the piece
                    board.freezePiece(piece.getFigure(), piece.xShift, piece.yShift)
                    # Create a new piece
                    piece = Piece(piece_start_XPos, piece_start_YPos)
                    # Check for game over
                    if board.intersects(piece.getFigure(), piece.xShift, piece.yShift):
                        state = "gameover"
            else:
                running = False


        # piece = Piece(pieceStartXPos, pieceStartYPos)
        # Check intersection to see if the player has lost
        if board.intersects(piece.getFigure(), piece_start_XPos, piece_start_YPos):
            state = "" #TODO: Change game state

        renderer.renderBoard(board)

        renderer.drawPiece(piece)

        # refresh the screen
        pygame.display.flip()
        clock.tick(fps)
    
    pygame.quit()

if __name__ == "__main__":
    run_game()