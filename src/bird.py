# Import required libraries
import pygame
import os
from os.path import dirname, abspath

from Game import Game
# Load in required images and double their size
imgs_path = dirname(dirname(abspath(__file__)))

BIRD_ASSETS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, "imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, "imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, "imgs", "bird3.png")))
]
# A Bird class to make the creation and handling of the bird and its behavior easier and more efficient using OOP
class Bird(Game):
    ASSETS = BIRD_ASSETS # All the images of the bird
    MAX_ROTATION = 25 # The angle of tilt of the bird when it moves up and down (image is rotated 25 degrees)
    ROTATION_VEL = 20 # How much the bird will be rotated per frame (i.e. every time it moves)
    ANIMATION_TIME = 5 # How long each bird animation will be shown (i.e. how fast it is flapping its wings)

    # The constructor for the Bird class, with 2 explicit parameters x and y and the object passed as an implicit paramater.
    def __init__(self, x, y):
        self.x = x # The initial x-coordinate of the bird.
        self.y = y # The initial y-coordinate of the bird.
        self.tilt = 0 # The initial tilt of the bird - 0 since it's looking straight ahead.
        self.tick_count = 0 # Tick count is used to determine when the bird last jumped. It represented how long the bird has been moving which is used in determining the velocity and direction of the bird.
        self.velocity = 0 # The initial velocity of the bird.
        self.height = self.y # The initial height of the bird, which is just the y-coordinate of its current position.
        self.img_count = 0 # The number of the image that will be displayed.
        self.img = self.ASSETS[self.img_count] # The image that will be displayed. 

    # This method makes the bird 'jump' i.e. move up on the screen
    def jump(self):
        self.velocity = -10.5 # In order to move up, the velocity has to be negative, as (0,0) is located at the top-left
        self.tick_count = 0 # Since bird has jumped, reset tick_count
        self.height = self.y # Set the current height of the bird as its current y-coordinate
    
    # This method makes the bird actually move and handles the physics
    def move(self):
        TERMINAL_VELOCITY = 16 # The maximum velocity of the bird
        GRAVITY = 3 # The acceleration the bird experiences due to gravity
        self.tick_count += 1 # Increment tick_count since a frame went by and the bird moved without jumping
        displacement = self.velocity * self.tick_count + 0.5 * GRAVITY * (self.tick_count ** 2) # The number of pixels moved up or down in this frame
        # Displacement calculation comes from the kinematics equation, Δd = viΔt + 0.5a(Δt^2)
        # Based on the current velocity and how much time has passed since its last jump, we can compute the vertical displacement.
        # Allows us to get a parabolic trajectory on the bird to emulate realism

        # If the amount of pixels in the vertical displacement is greater than the terminal velocity permits, set the displacement to the terminal velocity. 
        if displacement >= TERMINAL_VELOCITY:
            displacement = TERMINAL_VELOCITY
        
        # If the displacement is negative (i.e. moving upwards), moves the bird slightly higher in order to fine-tune the movement
        if displacement < 0:
            displacement -= 2
        
        # Increment the current y-position of the bird by the displacement. 
        self.y += displacement

        # If the displacement is negative (i.e. moving upwards) or the bird's position is above its initial jump position, tilt the bird upwards
        if displacement < 0 or self.y < self.height + 50:
            # If the current tilt of the bird is less than the max allowable tilt, set the bird's tilt to the maximum tilt
            if self.tilt < self.MAX_ROTATION:
                # The bird has now been rotated by MAX_ROTATION degrees counter-clockwise
                self.tilt = self.MAX_ROTATION 
        # Otherwise, the bird must be moving downwards, so the bird should be tilting downwards. 
        else:
            # If the current tilt of the bird is greater than 90 degrees (i.e. the bird is not facing the ground completely), decrease its tilt by the rotation velocity
            if self.tilt > -90:
                # The bird gradually tilts more and more downwards until it is facing 90 degrees from its original position
                self.tilt -= self.ROTATION_VEL
    
    def draw(self, window):
        self.img_count += 1 # Keeps track of the amount of ticks an image has been shown for

        # This section chooses which bird image to display based on how long the previous image has been shown for to produce a smooth flapping animation. 
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.ASSETS[0] # Show the bird with its wings up if the image count is less than the animation time
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.ASSETS[1] # Transition to the bird with its wings at its side
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.ASSETS[2] # Transition to the bird with its wings down
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.ASSETS[1] # Transition to the bird with its wings at its side
        elif self.img_count == self.ANIMATION_TIME *4 + 1:
            self.img = self.ASSETS[0] # Finally, transition to the bird with its wings up, completing the flapping animation loop
            self.img_count = 0 # Resest the image count
        
        # If the bird is tilted almost completely downwards, there should be no flapping animation. 
        # Thus, the bird will have its wings by its side and the image count is set to double the animation time
        if self.tilt <= -80:
            self.img = self.ASSETS[1] # Set the current bird image to the image with the wings at its side
            self.img_count = self.ANIMATION_TIME * 2 # This ensures that when the flapping animation resumes, it's a smooth transition between image 2 and 3
    
        # This section actually rotates the bird image from the specified angle of tilt
        # Since Pygame rotates about the top-left corner, additional code is required to rotate about the center of the bird
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotated_img, new_rect.topleft)

    # A method that stores a 2-Dimensional list of the location of all the pixels of an image
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
