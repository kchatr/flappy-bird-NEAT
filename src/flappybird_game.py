"""
A large part of this program was inspired by Tech with Tim's GitHub repo https://github.com/techwithtim/NEAT-Flappy-Bird and his video series.
It has been modified and added onto significantly, but the assets and and core logic are motivated from TWT's tutorial.
No line of code has been written, however, without my explicit understanding of what it does and why it is there.
I hope you enjoy my reanimation of a classic game :D
- Kaushik Chatterjee (kchatr)
"""

# Import required libraries
import pygame
import neat
import time
import os
from os.path import dirname, abspath
import random
import pickle

from bird import Bird
from pipe import Pipe
from base import Base


pygame.font.init()
SCORE_FONT = pygame.font.SysFont("comicsans", 50) # The font for the score

WIN_WIDTH = 575 # The width of the game window
WIN_LENGTH = 800 # The length of the game window

imgs_path = dirname(dirname(abspath(__file__)))

BACKGROUND_ASSET = random.choice([pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, "imgs", "bg.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, "imgs", "bg_night.jpeg")))]) # Load in the game's background



# A method that draws the Start window of the game
def draw_window_start(window):
    window.blit(BACKGROUND_ASSET, (0, 0)) # The blit method actually 'draws' the background image to the game window
    
    # These sequential statements create and render the desired text to the Pygame window.
    # They are initialized with the appropriate font and size to the center of the screen
    intro = pygame.font.SysFont("comicsans", 26).render(f"This is classic Flappy Bird recreated, with a few extra dimensions!", 1, (255, 255, 255)) 
    intro_rect = intro.get_rect()
    intro_rect.center = (WIN_WIDTH / 2, WIN_LENGTH / 2 - 300)
    window.blit(intro, intro_rect)

    menu = pygame.font.SysFont("comicsans", 30).render(f"Press M to open the game menu.", 1, (255, 255, 255)) 
    menu_rect = menu.get_rect()
    menu_rect.center = (WIN_WIDTH / 2, WIN_LENGTH / 2 - 240)
    window.blit(menu, menu_rect)

    option_1 = pygame.font.SysFont("comicsans", 28).render(f"1) PLAY - Play the Game", 1, (255, 255, 255)) 
    option_1_rect = option_1.get_rect()
    option_1_rect.center = (WIN_WIDTH / 2 - 5, WIN_LENGTH / 2 - 150)
    window.blit(option_1, option_1_rect)

    option_2 = pygame.font.SysFont("comicsans", 28).render(f"2) LEARN - Witness the power of neural networks", 1, (255, 255, 255)) 
    option_2_rect = option_2.get_rect()
    option_2_rect.center = (WIN_WIDTH / 2 - 10, WIN_LENGTH / 2 - 125)
    window.blit(option_2, option_2_rect)
    
    option_3 = pygame.font.SysFont("comicsans", 28).render(f"3) TRAIN - Train an invincible bird with AI", 1, (255, 255, 255)) 
    option_3_rect = option_3.get_rect()
    option_3_rect.center = (WIN_WIDTH / 2 - 15, WIN_LENGTH / 2 - 100)
    window.blit(option_3, option_3_rect)

    options = pygame.font.SysFont("comicsans", 30).render(f"Please press 1, 2, or 3 on your keyboard.", 1, (255, 255, 255)) 
    options_rect = options.get_rect()
    options_rect.center = (WIN_LENGTH / 2 - 100, WIN_LENGTH / 2)
    window.blit(options, options_rect) 

    pygame.display.update() # Update the game window's display

# Creates the menu screen which displays the instructions and explains the options to the user.
def draw_menu(window):
    window.blit(BACKGROUND_ASSET, (0, 0)) # The blit method actually 'draws' the background image to the game window

    # These sequential statements create and render the desired text to the Pygame window.
    # They are initialized with the appropriate font and size to the center of the screen
    menu = pygame.font.SysFont("comicsans", 27).render(f"1) Your turn! Press SPACE to make the bird jump vertically.", 1, (255, 255, 255)) 
    window.blit(menu, (30, 50)) 

    menu = pygame.font.SysFont("comicsans", 30).render(f"Avoid the pipes and the ground!", 1, (255, 255, 255)) 
    window.blit(menu, (30, 70)) 

    menu = pygame.font.SysFont("comicsans", 30).render(f"2) Learn how an AI does it!", 1, (255, 255, 255)) 
    window.blit(menu, (30, 120)) 

    menu = pygame.font.SysFont("comicsans", 30).render(f"Press Q at any time to quit.", 1, (255, 255, 255)) 
    window.blit(menu, (30, 140)) 

    menu = pygame.font.SysFont("comicsans", 30).render(f"3) Train your own AI and watch those birds go!", 1, (255, 255, 255)) 
    window.blit(menu, (30, 190)) 
    
    menu = pygame.font.SysFont("comicsans", 30).render(f"Press Q at any time to quit.", 1, (255, 255, 255)) 
    window.blit(menu, (30, 210)) 

    menu = pygame.font.SysFont("comicsans", 32).render(f"Press SPACE to go to the home screen.", 1, (255, 255, 255)) 
    window.blit(menu, (30, 260)) 

    pygame.display.update() # Update the game window's display


    choice = False # A boolean variable that tracks whether or not the user made a choice

    # While the user has not made a choice:
    while not choice:
        # Continually keep track of any events (i.e. key presses) from the user
        for event in pygame.event.get():
            # If the user chooses to close the Pygame window, quit the game and set choice to True
            if event.type == pygame.QUIT:
                choice = True # Set the choice to True
            # If the user presses the SPACE key, go back to the main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()


# Creates the ending window when the game ends (i.e. the user's bird crashes)
def draw_window_end(window):
    window.blit(BACKGROUND_ASSET, (0, 0)) # The blit method actually 'draws' the background image to the game window
    
    # The same process as above for generating the text and then displaying it to the user on the game window. 
    end = pygame.font.SysFont("comicsans", 24).render(f"Game over! Press 'SPACE' to play again and any key to quit.", 1, (255, 255, 255)) 
    end_rect = end.get_rect()
    end_rect.center = (WIN_WIDTH / 2, WIN_LENGTH / 2 - 100)
    window.blit(end, end_rect)

    pygame.display.update() # Update the game window's display

    choice = False # A boolean variable that tracks whether or not the user made a choice

    # While the user has not made a choice:
    while not choice:
         # Continually keep track of any events (i.e. key presses) from the user
        for event in pygame.event.get():
            # If the user chooses to close the Pygame window, quit the game and set choice to True
            if event.type == pygame.QUIT:
                choice = True
            # If the user presses the SPACE key, go back to the main menu; otherwise, quit from the game 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                else:
                    pygame.quit()

# Method to draw the game window for the birds AI to be trained
def draw_window(window, birds, pipes, base, score, cur_gen):
    window.blit(BACKGROUND_ASSET, (0, 0)) # The blit method actually 'draws' the background image to the game window

    score_display = SCORE_FONT.render(f"Score: {score}", 1, (255, 255, 255)) # Renders the score of either the user or the AI in the game state
    window.blit(score_display, (WIN_WIDTH - 10 - score_display.get_width(), 10)) # Draws the score onto the game window
    
    score_display = SCORE_FONT.render(f"Gen: {cur_gen}", 1, (255, 255, 255)) # Renders the current generation of birds
    window.blit(score_display, (10, 10)) # Draws the generations onto the game window

    # Pipes is a list storing the top and bottom pipe.
    # This for loop draws them to the game window using the previously defined draw method in the Pipe class
    for pipe in pipes:
        pipe.draw(window)
    
    base.draw(window) # Draw the base (the ground) using the previously defined draw method in the Base class

    for bird in birds:
        bird.draw(window) # Draw the bird using the previously defined draw method in the Bird class

    pygame.display.update() # Update the game window's display

# Method to draw the game window for a game played by the user.
def draw_window_classic(window, bird, pipes, base, score):
    window.blit(BACKGROUND_ASSET, (0, 0)) # The blit method actually 'draws' the background image to the game window

    score_display = SCORE_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    window.blit(score_display, (WIN_WIDTH - 10 - score_display.get_width(), 10))

    # Pipes is a list storing the top and bottom pipe, and this draws them to the game window using the previously defined draw method
    for pipe in pipes:
        pipe.draw(window)
    
    base.draw(window) # Draw the base (the  ground) using the previously defined draw method

    bird.draw(window) # Draw the bird using the previously defined draw method

    pygame.display.update() # Update the display

# Initialize a classic game, that is played by the user and analogous to the original game itself (i.e. the PLAY option)
def classic_game():
    bird = Bird(230, 350) # Initialize a bird object
    base = Base() # Initialize the base object
    pipes = [Pipe(WIN_WIDTH)] # A list that keeps track of the current pipes
    window = pygame.display.set_mode((WIN_WIDTH, WIN_LENGTH)) # Initialize the window
    clock = pygame.time.Clock() # Sets the frame rate i.e. the tick rate of the game
    user_score = 0 # The current score of the user

    play_game = True # A boolean variable that tracks whether the game should continue to run

    # While the user has not quit or failed:
    while play_game:
        clock.tick(30) # A maximum of 30 ticks every second
        # For each event (i.e. a keyboard trigger, mouse click, etc.):
        for event in pygame.event.get():
            # If the user hits the X in the Pygame window, exit the game and terminate the program
            if event.type == pygame.QUIT:
                play_game = False
            # Otherwise, if the user presses SPACE, make the bird jump
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        
        add_pipe = False # Keeps track of whether or not to add a new pipe to the game window
        removed_pipes = [] # A list to store the pipes that need to be removed
        
        # Call the move method defined for each pipe object that currently exists
        # Pipes is a list storing the top and bottom pipe, and this draws them to the game window using the previously defined draw method
        for pipe in pipes:
            # If the bird collides with a pipe or falls off the screen, terminate the current game
            if pipe.collide(bird) == True or (bird.y + bird.img.get_height() >= base.y or bird.y < 0):
                play_game = False
            else:
                # If the pipe is now completely off the screen, add it to the list of pipes to be removed
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    removed_pipes.append(pipe)
            
                # If the bird has passed the pipe and the pipe has not been passed before, we need to draw a new pipe
                if not pipe.bird_passed and pipe.x < bird.x:
                    pipe.bird_passed = True
                    add_pipe = True
                
                # Move the pipes leftwards
                pipe.move()
        
        # If the user has passed the set of pipes, increment their score and add the pipes to the list to be removed
        if add_pipe:
            user_score += 1
            pipes.append(Pipe(WIN_WIDTH))
        for rem in removed_pipes:
            pipes.remove(rem)
        if bird.y + bird.img.get_height() >= base.y:
            pass
        
        bird.move() # Call the move method defined for a bird object
        base.move() # Call the move method defined for a base object 

        draw_window_classic(window, bird, pipes, base, user_score) # Draw the game window
    
    window = pygame.display.set_mode((WIN_WIDTH, WIN_LENGTH)) # Initialize the window
    draw_window_end(window)

# A game played by a previously trained AI bird (i.e. the LEARN option)
def ai_game():
    trained_bird = open("C:\Projects\Flappy-Bird-NEAT\\best_bird.pickle", "rb") # Open the save neural network file
    bird_neural_network = pickle.load(trained_bird) # Load in the deserialized object using pickle
    bird = Bird(230, 350) # Initialize the bird object
    base = Base() # Initialize the base
    pipes = [Pipe(WIN_WIDTH)] # A list that keeps track of the current pipes
    window = pygame.display.set_mode((WIN_WIDTH, WIN_LENGTH)) # Initialize the window
    clock = pygame.time.Clock() # Sets the frame rate i.e. the tick rate of the game
    bird_score = 0 # The score of the bird

    play_game = True # A boolean variable that tracks whether the game should continue to run

    # While the user has not quit the game:
    while play_game:
        clock.tick(30) # A maximum of 30 ticks every second
        # For each event (i.e. a keyboard trigger, mouse click, etc.):
        for event in pygame.event.get():
            # If the user hits the X in the Pygame window, exit the game and terminate the program
            if event.type == pygame.QUIT:
                play_game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
        
        # The index of the pipe inputted into the neural network
        pipe_index = 0
        
        # If the bird has already passed the 1st pipe in the list, then set pipe_index to the 2nd 
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_index = 1
        
        # Continually move the bird
        bird.move()
        
        # The output of the neural network based on the position of the bird relative to the pipes
        nn_output = bird_neural_network.activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom_pipe)))
        
        # If the output of the network is greater than 0.5, make the bird jump
        if nn_output[0] > 0.5:
            bird.jump()

        
        add_pipe = False # Keeps track of whether or not to add a new pipe to the game window
        removed_pipes = [] # A list to store the pipes that need to be removed
        # Call the move method defined for each pipe object that currently exists
        # Pipes is a list storing the top and bottom pipe, and this draws them to the game window using the previously defined draw method
        for pipe in pipes:
            if pipe.collide(bird) == True or (bird.y + bird.img.get_height() >= base.y or bird.y < 0):
                play_game = False
            else:
                # If the pipe is now completely off the screen, add it to the list of pipes to be removed
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    removed_pipes.append(pipe)
            
                # If the bird has passed the pipe and the pipe has not been passed before, we need to draw a new pipe
                if not pipe.bird_passed and pipe.x < bird.x:
                    pipe.bird_passed = True
                    add_pipe = True
                
                # Move the pipes leftward
                pipe.move()
        
        # If the bird has passed the set of pipes, increment their score and add the pipes to the list to be removed
        if add_pipe:
            bird_score += 1
            pipes.append(Pipe(WIN_WIDTH))
        for rem in removed_pipes:
            pipes.remove(rem)
        if bird.y + bird.img.get_height() >= base.y:
            pass

        base.move() # Call the move method defined for a base object 

        draw_window_classic(window, bird, pipes, base, bird_score) # Draw the game window

# The current generation of the birds being trained
CUR_GEN = 1
# A game where the birds are trained and the user can view the training (i.e. the TRAIN option)
def gen_training(genomes, config):
    global CUR_GEN # Declare global variables
    cur_neural_networks = [] # A list that stores all the neural networks for each bird being trained
    cur_genomes = [] # A list that stores the fitness for all the birds
    birds = [] # A list that stores all the birds 

    # Iterate through genomes and initialize the birds, along with their fitness and neural network
    for _, g in genomes:
        g.fitness = 0
        neural_network = neat.nn.FeedForwardNetwork.create(g, config)
        cur_neural_networks.append(neural_network)
        birds.append(Bird(230, 350))
        cur_genomes.append(g)
        

    base = Base() # Create the base object
    pipes = [Pipe(WIN_WIDTH)] # A list that keeps track of the current pipes
    window = pygame.display.set_mode((WIN_WIDTH, WIN_LENGTH)) # Initialize the window
    clock = pygame.time.Clock() # Sets the frame rate i.e. the tick rate of the game
    score = 0 # The score of the best bird of the generation

    play_game = True # A boolean variable that tracks whether the game should continue to run

    # While the user has not quit
    while play_game:
        clock.tick(30) # A maximum of 30 ticks every second
        # For each event (i.e. a keyboard trigger, mouse click, etc.):
        for event in pygame.event.get():
            # If the user hits the X in the Pygame window, exit the game and terminate the program
            if event.type == pygame.QUIT:
                play_game = False
                pygame.quit() # Quit the Pygame window
                quit() # Quit the program
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
        
        pipe_index = 0 # The index of the pipe to be inputted into the neural network
        # If the birds list is not empty, set pipe_index to 1 (the second pipe in the list) if the bird has already passed the first pipe
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            run = False
            break
        
        # A for loop to iterate through the birds and modify their fitness
        # Computes and stores the neural network's output to decide if a bird should jump
        for x, bird in enumerate(birds):
            cur_genomes[x].fitness += 0.1
            bird.move()
            
            nn_output = cur_neural_networks[x].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom_pipe)))

            if nn_output[0] > 0.5:
                bird.jump()

        
        add_pipe = False # Keeps track of whether or not to add a new pipe to the game window
        removed_pipes = [] # A list to store the pipes that need to be removed
        # Call the move method defined for each pipe object that currently exists
        # Pipes is a list storing the top and bottom pipe, and this draws them to the game window using the previously defined draw method
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird) == True:
                    cur_genomes[i].fitness -= 1
                    birds.pop(i)
                    cur_neural_networks.pop(i)
                    cur_genomes.pop(i)

                # If the bird has passed the pipe and the pipe has not been passed before, we need to draw a new pipe
                if not pipe.bird_passed and pipe.x < bird.x:
                    pipe.bird_passed = True
                    add_pipe = True
                    
            # If the pipe is now completely off the screen, add it to the list of pipes to be removed
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removed_pipes.append(pipe)

            # Move the pipe leftward    
            pipe.move()
        
        # If the bird has passed the set of pipes, increment their score and add the pipes to the list to be removed
        # Their fitness is also incremented by 5, motivating them to pass pipes to make it as far as possible
        if add_pipe:
            score += 1
            for g in cur_genomes:
                g.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))
        for rem in removed_pipes:
            pipes.remove(rem)
        
        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= base.y or bird.y < 0:
                birds.pop(i)
                cur_neural_networks.pop(i)
                cur_genomes.pop(i)
        
        base.move() # Call the move method defined for a base object

        # If the birds score is over 150, make them the new best bird and save them to a file, and terminate the game
        if score > 150:
            pickle.dump(cur_neural_networks[0], open("best_bird.pickle", "wb"))
            play_game = False
            break

        draw_window(window, birds, pipes, base, score, CUR_GEN) # Draw the game window

# Initializes the neural network and the parameters for the NEAT algorithm
# This was created by following the NEAT libraries official documentation, 
def run(config_file):
    # Initialize the configuration file for the neural network & algorithm's parameters
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    population = neat.Population(config) # Sets the population of a generation
    
    population.add_reporter(neat.StdOutReporter(True)) # Provides stats regarding the current generation and fitness
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(gen_training, 64)

# The main method
def main():
    window = pygame.display.set_mode((WIN_WIDTH, WIN_LENGTH)) # Initialize the window
    
    draw_window_start(window) # Draw the start window

    choice = False # Boolean variable that tracks whether the user has made a choice or not
    
    # While the user has not made a choice:
    # Allow the user to press the appropriate key to make their selection and calling the corresponding method
    while not choice:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choice = True
                    classic_game()
                elif event.key == pygame.K_2:
                    choice = True
                    ai_game()
                elif event.key == pygame.K_3:
                    choice = True
                    config_file = os.path.join(os.path.dirname(__file__), "neatconfig.txt")
                    run(config_file) 
                elif event.key == pygame.K_m:
                    choice = True
                    draw_menu(window)

# Calls the program from the command line when run and handles any excpetions
if __name__ == '__main__':
    try:
        main()
    except pygame.error:
        quit()
    except:
        print("An error occurred. Restarting program...")
        main()