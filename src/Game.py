from abc import ABC, abstractmethod

# An interface implemented in Python that forms a solid blueprint for any game to be developed
class Game(ABC):

    # An abstract method that will draw the sprite onto the game window
    @abstractmethod
    def draw(self, window):
        pass
    
    # An abstract method that will move the sprite
    @abstractmethod
    def move(self):
        pass