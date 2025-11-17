"""
Author: Nathaniel Brewer


"""
import pygame# type: ignore (ignores the "could not resolve" error)

from .abstract_state import States

class Pause(States):
    def __init__(self, config, input, renderer):
        States.__init__(self, config, input, renderer)
        self.next = 'pause'

        # Injected Dependencies
        self.config = config
        self.input = input
        self.renderer = renderer

        self.drawn = False

        # Game over buttons
        self.buttons = [
            {"label": "Resume", "rect": pygame.Rect(100, 80, 200, 50), "action": "game"},
            {"label": "Restart", "rect": pygame.Rect(100, 150, 200, 50), "action": "restart"},
            {"label": "Settings", "rect": pygame.Rect(100, 220, 200, 50), "action": "settings"},
            {"label": "Return to Menu", "rect": pygame.Rect(100, 290, 200, 50), "action": "menu"},
        ]

    def cleanup(self):
        self.renderer.clear();
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
                        return button["action"]
        if(not self.drawn):
            # Only need to draw button states once
            self.draw()
            self.drawn = True
        return 'pause'
    def draw(self):
        self.renderer.clear()

        self.renderer.render_pause(self.buttons)