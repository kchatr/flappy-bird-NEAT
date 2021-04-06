from abc import ABC, abstractmethod

class Game(ABC):

    @abstractmethod
    def draw(self, window):
        pass
    
    @abstractmethod
    def move(self):
        pass