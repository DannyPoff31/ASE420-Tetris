"""
    Author: Nathaniel Brewer

    Menu state, child of abstract_state. Handles all things to do on the menu and returns the desired location to the state_manager
"""
import pygame # type: ignore
from .abstract_state import AbstractState

class Menu(AbstractState):
    def __init__(self, config, input, renderer):
        super().__init__(config, input, renderer)
        self.next = 'game'

        self.drawn = False
        
        # Menu buttons
        self.buttons = [
            {"label": "Start Game", "rect": pygame.Rect(100, 100, 200, 50), "action": "gamemode"},
            {"label": "Settings", "rect": pygame.Rect(100, 170, 200, 50), "action": "settings"},
            {"label": "Quit", "rect": pygame.Rect(100, 240, 200, 50), "action": "quit"}
        ]

    def cleanup(self):
        self.renderer.clear()
        self.startup()

    def startup(self):
        self.drawn = False

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        # Play click sound when button is clicked
                        self.config.play_click_sound()
                        return button["action"]
        if(not self.drawn):
            # Only need to draw button states once
            self.draw()
            self.drawn = True
        return 'menu'

    def draw(self):
        # Clear screen
        self.renderer.clear()

        # Render the main menu
        self.renderer.render_menu(self.buttons)
