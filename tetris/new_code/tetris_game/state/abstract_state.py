"""
    Author: Nathaniel Brewer

    This is the abstract class that all states will have to overwrite
"""

from abc import ABC, abstractmethod

class AbstractState(ABC):
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
    
    @abstractmethod
    def startup(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass
