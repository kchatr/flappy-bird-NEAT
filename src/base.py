import pygame
import os

from Game import Game
# A Base class to handle the creation and logic of the base (i.e. the ground) in the game
class Base(Game):
    GROUND_ASSET = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "ground.png"))) # Load in required images and double their size

    VELOCITY = 5 # The velocity of the moving base, which is equal to that of the pipes
    WIDTH = GROUND_ASSET.get_width() # THe width of the base
    IMG = GROUND_ASSET # Alias for the image of the base

    def __init__(self):
        self.y = 730 # The y-position of the base
        self.x1 = 0 # The x position of the first base
        self.x2 = self.WIDTH # The x position of the second base, directly behind the first

    # A method that actually moves each base in order to give the appearance of an infinite scroller.
    # There are two bases, each the width of the game window. As one moves to the left, so does the other one.
    # When a base is completely off-screen, it is pushed behind the second and 'recycled'.
    # This process continues to repeat while the game is running.
    def move(self):
        self.x1 -= self.VELOCITY # Move the first base to the left at the specified velocity
        self.x2 -= self.VELOCITY # Move the second base to the left at the specified velocity

        # If the first base is completely off the screen, move it to the back of the second base
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        # If the second base is completely off the screen, move it to the back of the first base
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))