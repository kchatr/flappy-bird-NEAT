# Import required libraries
import pygame
import os
from os.path import dirname, abspath

from Game import Game

imgs_path = dirname(dirname(abspath(__file__)))

GROUND_ASSET = pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, "imgs", "ground.png"))) # Load in required images and double their size

# A Base class to make the creation and handling of the base (i.e. ground) and its behavior easier and more efficient using OOP
class Base(Game):
    VELOCITY = 5 # The velocity of the moving base, which is equal to that of the pipes
    WIDTH = GROUND_ASSET.get_width() # THe width of the base
    IMG = GROUND_ASSET # Alias for the image of the base

    # The constructor for the Base class, with the object passed as an implicit paramater.
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
    
    # Draw both bases onto the game window to ensure it appears as an infinite scroller.
    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))