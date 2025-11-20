"""
Author: Nathaniel Brewer
"""
import pygame # type: ignore (ignores the "could not resolve" error)

from ..ui.renderer import Renderer

from ..input.input import Input

from ..config.config import Config

from ..state.enhanced_state_manager import EnhancedStateManager

def run_game():

    def quit_game():
        nonlocal running
        running = False
    
    # Begin the config process 
    config = Config()

    # Start the pygame client
    pygame.init()
    screen = pygame.display.set_mode((config.window_width, config.window_height))
    pygame.display.set_caption("Code^3 Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans', 25, True, False)

    # What creates the screen
    renderer = Renderer(screen = screen)

    # Create input
    input = Input(config)

    # Create the abstract state class to be handled throughout the loop
    state_manager = EnhancedStateManager(config, input, renderer)

    # Main run Bool
    running = True

    # Main Run loop
    while running:

        config.counter += config.level
        if config.counter > 100000:
            config.counter = 0

        # Update the current state to update the screen. IF returns false then the game will quit
        running = state_manager.update()

        # refresh the screen
        pygame.display.flip()
        clock.tick(config.fps)
    
    pygame.quit()

if __name__ == "__main__":
    run_game()