"""
    Author: Nathaniel Brewer
"""
import pygame # type: ignore
from .abstract_state import States

class GamemodeSelection(States):
    def __init__(self, config, input, renderer):
        super.__init__(self, config, input, renderer)
        self.next = 'game'

        self.drawn = False

    def cleanup(self):
        self.renderer.clear()

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
        self.rendereer.clear()

        self.renderer.render_gamemode_screen()
        pass
