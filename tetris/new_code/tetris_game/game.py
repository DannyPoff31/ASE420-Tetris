import pygame

from board import Board
from renderer import Renderer
from piece import Piece
from input import Input

# The size of the play screen
size = (400, 500)

def run_game():

    #Create input handler
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Code^3 Tetris")
    clock = pygame.time.Clock()

    # What creates the screen
    renderer = Renderer(screen = screen)

    #change to menu/settings/etc
    state = "start"

    running = True  # Main run Bool

    playing = False # When starting to play the actial game

     # Create input
    input = Input()

    fps = 25
    counter = 0
    pressing_down = False

    height = 20
    width = 10

    font = pygame.font.SysFont('Comic Sans', 25, True, False)

    #Create new instance of board
    board = Board(height, width)

    #Default starting position for pieces
    pieceStartXPos = 3
    pieceStartYPos = 0
    piece = Piece(pieceStartXPos, pieceStartYPos)

    while running:

        counter += 1
        if counter > 100000:
            counter = 0

        # Check if we need to automatically go down
        if counter % (fps // 2) == 0 or pressing_down:
            if state == "start":
                if not board.intersects(piece.getFigure(), piece.xShift, piece.yShift + 1):
                    piece.yShift += 1
                else:
                    # Freeze the piece
                    board.freezePiece(piece.getFigure(), piece.xShift, piece.yShift)
                    # Create a new piece
                    piece = Piece(pieceStartXPos, pieceStartYPos)
                    # Check for game over
                    if board.intersects(piece.getFigure(), piece.xShift, piece.yShift):
                        state = "gameover"
            else:
                running = False


        # This is what checks what keys are being pressed
        # Returns True if key is pressed down, false otherwise
        # TODO: Might be a better way to do this?
        pressing_down = input.event_handler(piece, board)

        # piece = Piece(pieceStartXPos, pieceStartYPos)
        # Check intersection to see if the player has lost
        if board.intersects(piece.getFigure(), pieceStartXPos, pieceStartYPos):
            state = "" #TODO: Change game state

        renderer.renderBoard(board)

        renderer.drawPiece(piece)

        # refresh the screen
        pygame.display.flip()
        clock.tick(fps)
    
    pygame.quit()

if __name__ == "__main__":
    run_game()