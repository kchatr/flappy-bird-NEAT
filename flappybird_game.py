import pygame
import neat
import time
import os
import random

pygame.font.init()

WIN_WIDTH = 575 # The width of the game window
WIN_LENGTH = 800 # The length of the game window

# Load in all of the images used in the game (i.e. the assets)
# Images are doubled in size and loaded in from the filepath
BIRD_ASSETS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_ASSET = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
GROUND_ASSET = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "ground.png")))
BACKGROUND_ASSET = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

# A Bird class to make the handling of the bird and its behavior easier and efficient
class Bird:
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
        self.tick_count += 1 # Increment tick_count since a frame went by and the bird moved without jumping
        displacement = self.velocity * self.tick_count + 0.5 * 3 * (self.tick_count ** 2) # The number of pixels moved up or down in this frame
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

class Pipe:
    SPACE = 200 # The space in between the top and bottom pipe
    VELOCITY = 5 # The pipes are what move backwards, not the bird moving forward - the bird doesn't actually have any horizontal velocity

    def __init__(self):
        self.x = WIN_WIDTH # The x location of the pipe, which is at the edge of the window
        self.height = 0 # The height of the pipe
        self.top_pipe = 0 # Location of the top of the pipe
        self.bottom_pipe = 0 # Location of the bottom of the pipe
        self.PIPE_TOP = pygame.transform.flip(PIPE_ASSET, False, True) # The pipe at the top of the screen, which is flipped
        self.PIPE_BOTTOM = PIPE_ASSET # The pipe on the bottom of the screen 
        self.bird_passed = False # Keeps track if the bird has already passed the pipe
        self.set_height() # Sets the height of the pipe and the location of it
    
    def set_height(self):
        self.height = random.randrange(40, 450) # The height of the pipe, which is a random number between 40 and 450
        self.top_pipe = self.height - self.PIPE_TOP.get_height() # If the pipe is on the top, this determines where the top of the pipe is
        self.bottom_pipe = self.height + self.SPACE # If the pipe is on the bottom, this determines where the bottom of the pipe is

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

class Base:
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

# Method to draw the game window
def draw_window(window, bird, pipes, base, score):
    window.blit(BACKGROUND_ASSET, (0, 0)) # The blit method actually 'draws' the background image to the game window

    score_display = SCORE_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    window.blit(score_display, (WIN_WIDTH - 10 - score_display.get_width(), 10))

    # Pipes is a list storing the top and bottom pipe, and this draws them to the game window using the previously defined draw method
    for pipe in pipes:
        pipe.draw(window)
    
    base.draw(window) # Draw the base (the ground) using the previously defined draw method

    bird.draw(window) # Draw the bird using the previously defined draw method

    pygame.display.update() # Update the display

# The main method which acts as a controller for the rest of the program
def main():
    bird = Bird(230, 350) # Initialize a bird object
    base = Base()
    pipes = [Pipe()]
    window = pygame.display.set_mode((WIN_WIDTH, WIN_LENGTH)) # Initialize the window
    clock = pygame.time.Clock() # Sets the frame rate i.e. the tick rate of the game
    user_score = 0

    play_game = True # A boolean variable that tracks whether the user wants to quit or continue playing

    # While the user still wants to play the game:
    while play_game:
        clock.tick(30) # A maximum of 30 ticks every second
        # For each event (i.e. a keyboard trigger, mouse click, etc.):
        for event in pygame.event.get():
            # If the user hits the X in the Pygame window, exit the game and terminate the program
            if event.type == pygame.QUIT:
                play_game = False
        
        add_pipe = False # Keeps track of whether or not to add a new pipe to the game window
        removed_pipes = [] # A list to store the pipes that need to be removed
        # Call the move method defined for each pipe object that currently exists
        # Pipes is a list storing the top and bottom pipe, and this draws them to the game window using the previously defined draw method
        for pipe in pipes:
            if pipe.collide(bird) == True:
                pass
            else:
                # If the pipe is now completely off the screen, add it to the list of pipes to be removed
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    removed_pipes.append(pipe)
            
                # If the bird has passed the pipe and the pipe has not been passed before, we need to draw a new pipe
                if not pipe.bird_passed and pipe.x < bird.x:
                    pipe.bird_passed = True
                    add_pipe = True
                
                pipe.move()
        
        if add_pipe:
            user_score += 1
            pipes.append(Pipe())
        for rem in removed_pipes:
            pipes.remove(rem)
        if bird.y + bird.img.get_height() >= base.y:
            pass
        
        # bird.move() # Call the move method defined for a bird object
        base.move() # Call the move method defined for a base object 

        draw_window(window, bird, pipes, base, user_score) # Draw the game window
    
    pygame.quit() # Quit the Pygame window
    quit() # Quit the program

if __name__ == '__main__':
    main()
            



