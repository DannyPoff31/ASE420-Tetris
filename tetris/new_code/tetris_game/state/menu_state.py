import pygame as pg
import sys
from .state import States

class Menu(States):
    def __init(self, config, input, renderer):
        States.__init__(self, config, input, renderer)
        self.next = 'game'

        # Injected dependencies
        self.config = config
        self.input = input
        self.renderer = renderer
        
        # State specific objects

    def cleanup(self):
        print("Cleaning up menu")
    def startup(self):
        print("starting menu")
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Game state keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,0,255))
