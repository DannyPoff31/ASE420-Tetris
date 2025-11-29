"""
    Author: Nathaniel Brewer

    Gameover state child of abstract_state, appears when the player loses
"""
import pygame # type: ignore (ignores the "could not resolve" error)
from .abstract_state import AbstractState

class GameOver(AbstractState):
    def __init__(self, config, input, renderer):
        super.__init__(self, config, input, renderer)
        self.next = 'menu'

        self.drawn = False

        # Game over buttons
        self.buttons = [
            {"label": "Try Again", "rect": pygame.Rect(100, 170, 200, 50), "action": "restart"},
            {"label": "Return to Menu", "rect": pygame.Rect(100, 240, 200, 50), "action": "menu"}
        ]

    def cleanup(self):
        self.renderer.clear();
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
        return 'gameover'
    def draw(self):
        self.renderer.clear()

        # Create a simple "GAME OVER" text overlay
        font = pygame.font.SysFont('Arial', 72, True)  # Large, bold font
        text_surface = font.render('GAME OVER', True, (255, 0, 0))  # Red text
        
        # Center the text on the screen
        screen_rect = self.renderer.screen.get_rect()
        text_rect = text_surface.get_rect(center=(screen_rect.centerx, screen_rect.centery))
        
        # Draw the text
        self.renderer.screen.blit(text_surface, text_rect)

        self.renderer.render_gameover(self.buttons)
