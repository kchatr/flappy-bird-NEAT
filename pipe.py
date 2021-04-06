import pygame
import os
import random
# A Pipe class that handles the creation and behaviour of the pipe, as well as collision mechanics.
class Pipe:
    PIPE_ASSET = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png"))) # Load in required images and double their size
    GAP = 200 # The gap in between the top and bottom pipe that the bird flies through
    VELOCITY = 5 # The pipes are what move backwards, not the bird moving forward - the bird doesn't actually have any horizontal velocity

    def __init__(self, width):
        self.x = width # The x location of the pipe, which is at the edge of the window
        self.height = 0 # The height of the pipe
        self.top_pipe = 0 # Location of the top of the pipe
        self.bottom_pipe = 0 # Location of the bottom of the pipe
        self.PIPE_TOP = pygame.transform.flip(PIPE_ASSET, False, True) # The pipe at the top of the screen, which is flipped
        self.PIPE_BOTTOM = PIPE_ASSET # The pipe on the bottom of the screen 
        self.bird_passed = False # Keeps track if the bird has already passed the pipe
        self.set_height() # Sets the height of the pipe and the location of it
    
    def set_height(self):
        self.height = random.randrange(50, 450) # The height of the pipe, which is a random number between 40 and 450
        self.top_pipe = self.height - self.PIPE_TOP.get_height() # If the pipe is on the top, this determines where the top of the pipe is
        self.bottom_pipe = self.height + self.GAP # If the pipe is on the bottom, this determines where the bottom of the pipe is

    def move(self):
        self.x -= self.VELOCITY # Move the pipe to the left based on the velocity
    
    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top_pipe)) # Draws the top pipe
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom_pipe)) # Draws the bottom pipe
    
    def collide(self, bird):
        bird_mask = bird.get_mask() # Gets the mask for the bird
        top_pipe_mask = pygame.mask.from_surface(self.PIPE_TOP) # Gets the mask for the top pipe
        bottom_pipe_mask = pygame.mask.from_surface(self.PIPE_BOTTOM) # Gets the mask for the bottom pipe

        # Offsets compute how far away the bird mask is from a pipe mask
        top_pipe_offset = (self.x - bird.x, self.top_pipe - round(bird.y)) # Stores the offset between the bird and the top pipe
        bottom_pipe_offset = (self.x - bird.x, self.bottom_pipe - round(bird.y)) # Stores the offset between the bird and the bottom pipe

        top_collision_point = bird_mask.overlap(top_pipe_mask, top_pipe_offset) # Will be None if there is no overlap between the bird mask and the top pipe
        bottom_collision_point = bird_mask.overlap(bottom_pipe_mask, bottom_pipe_offset) # Will be None if there is no overlap between the bird mask and the bottom pipe

        # If bottom_collision_point and top_collision_point are not none, a collision occurred and return True; else return False
        if bottom_collision_point != None or top_collision_point != None:
            return True
        else:
            return False
