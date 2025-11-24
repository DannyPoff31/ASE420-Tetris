"""
    Author: Nathaniel Brewer

    Pause state, child of abstract_state, handled by the enhanced_game_state to maintain the current game state.
"""
import pygame# type: ignore (ignores the "could not resolve" error)

from .state import States

class Pause(States):
    def __init__(self, config, input, renderer):
        States.__init__(self, config, input, renderer)
        self.next = 'pause'

        # Injected Dependencies
        self.config = config
        self.input = input
        self.renderer = renderer

        self.drawn = False

        # Pause menu buttons - centered with spacing
        button_width = 200
        button_height = 50
        button_spacing = 10
        center_x = self.config.window_width // 2
        
        self.buttons = [
            {"label": "Resume", "rect": pygame.Rect(center_x - button_width // 2, 120, button_width, button_height), "action": "game"},
            {"label": "Restart", "rect": pygame.Rect(center_x - button_width // 2, 120 + button_height + button_spacing, button_width, button_height), "action": "restart"},
            {"label": "Return to Menu", "rect": pygame.Rect(center_x - button_width // 2, 120 + (button_height + button_spacing) * 2, button_width, button_height), "action": "menu"},
        ]

    def cleanup(self):
        self.renderer.clear()
        self.drawn = False

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
<<<<<<< Updated upstream
=======
                        # Play click sound when button is clicked
                        self.config.play_click_sound()
>>>>>>> Stashed changes
                        return button["action"]
        if(not self.drawn):
            # Only need to draw button states once
            self.draw()
            self.drawn = True
        return 'pause'
    def draw(self):
        self.renderer.clear()

        self.renderer.render_pause(self.buttons)