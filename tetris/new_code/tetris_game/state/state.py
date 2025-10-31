"""
This is the abstract class that all states are children too
"""

import pygame as pg # type: ignore (ignores the "could not resolve" error)
import sys
from abc import ABC, abstractmethod

class States(ABC):
    def __init__(self, config, input, renderer):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

        self.config = config
        self.input = input
        self.renderer = renderer
    @abstractmethod
    def cleanup(self):
        pass
    def startup(self):
        pass
    def get_event(self, event):
        pass
    def update(self):
        pass
    def draw(self):
        pass
