import pygame # type: ignore (ignores the "could not resolve" error)

from game.board import Board
from game.piece import Piece
from game.piece_action import PieceAction

from ui.renderer import Renderer

from input.input import Input
from game.game_command import CommandFacotry

from config.config import Config

from state import StateManager

def run_game():

    def quit_game():
        nonlocal running
        running = False

    game_actions = {
        PieceAction.QUIT: quit_game,
    }


    
    # Begin the config process 
    config = Config()

    # Start the pygame client
    pygame.init()
    screen = pygame.display.set_mode(config)
    pygame.display.set_caption("Code^3 Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans', 25, True, False)

    # What creates the screen
    renderer = Renderer(screen = screen)

    # Create input
    input = Input(config)

    # Create the abstract state class to be handled throughout the loop
    state_manager = StateManager(config, input, renderer)

    # Main run Bool
    running = True

    # Main Run loop
    while running:

        if config.counter > 100000:
            config.counter = 0

        # Update the current state to update the screen
        state_manager.update(screen)

        # refresh the screen
        pygame.display.flip()
        clock.tick(config.fps)
    
    pygame.quit()

if __name__ == "__main__":
    run_game()