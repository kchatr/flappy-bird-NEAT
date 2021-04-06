import pygame
import neat
import time
import os
import random
import pickle

from bird import Bird
from pipe import Pipe
from base import Base

pygame.font.init()

WIN_WIDTH = 575 # The width of the game window
WIN_LENGTH = 800 # The length of the game window


BACKGROUND_ASSET = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

# Method to draw the game window
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

def classic_game():
    pass

def ai_game(genome, config):
    pass

CUR_GEN = 0
# The main method which acts as a controller for the rest of the program
def gen_training(genomes, config):
    global CUR_GEN
    CUR_GEN += 1
    cur_neural_networks = []
    cur_genomes = []
    birds = []

    for _, g in genomes:
        g.fitness = 0
        neural_network = neat.nn.FeedForwardNetwork.create(g, config)
        cur_neural_networks.append(neural_network)
        birds.append(Bird(230, 350))
        cur_genomes.append(g)
        

    base = Base()
    pipes = [Pipe(WIN_WIDTH)]
    window = pygame.display.set_mode((WIN_WIDTH, WIN_LENGTH)) # Initialize the window
    clock = pygame.time.Clock() # Sets the frame rate i.e. the tick rate of the game
    score = 0

    play_game = True # A boolean variable that tracks whether the game should continue to run

    # While the user still wants to play the game:
    while play_game:
        clock.tick(30) # A maximum of 30 ticks every second
        # For each event (i.e. a keyboard trigger, mouse click, etc.):
        for event in pygame.event.get():
            # If the user hits the X in the Pygame window, exit the game and terminate the program
            if event.type == pygame.QUIT:
                play_game = False
                pygame.quit() # Quit the Pygame window
                quit() # Quit the program
        
        pipe_index = 0 # The index of the pipe to be inputted into the neural network
        # If the birds list is not empty, set pipe_index to 1 (the second pipe in the list) if the bird has already passed the first pipe
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            run = False
            break
        
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
                
            pipe.move()
        
        if add_pipe:
            score += 1
            for g in cur_genomes:
                g.fitness += 5
            pipes.append(Pipe())
        for rem in removed_pipes:
            pipes.remove(rem)
        
        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= base.y or bird.y < 0:
                birds.pop(i)
                cur_neural_networks.pop(i)
                cur_genomes.pop(i)
        
        # bird.move() # Call the move method defined for a bird object
        base.move() # Call the move method defined for a base object

        if score > 100:
            pickle.dump(cur_neural_networks[0], open("best_bird.pickle", "wb"))
            play_game = False
            break

        draw_window(window, birds, pipes, base, score, CUR_GEN) # Draw the game window

def run(config_file):
    # Initialize the configuration file for the neural network & algorithm's parameters
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    population = neat.Population(config) # Sets the population of a generation
    
    population.add_reporter(neat.StdOutReporter(True)) # Provides stats regarding the current generation and fitness
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(gen_training, 64)

def main():
    print("This is an implementation of flappy bird!")
    print("There are 3 modes: Play (1); AI (2); Train (3).")
    choice = int(input("Please enter the number corresponding to your choice now.\n"))
    assert(choice in [1, 2, 3])
    
    if choice == 1:
        pass
    elif choice == 2:
        pass
    elif choice == 3:
        config_file = os.path.join(os.path.dirname(__file__), "neatconfig.txt")
        run(config_file) 


if __name__ == '__main__':
    config_file = os.path.join(os.path.dirname(__file__), "neatconfig.txt")
    main()
    run(config_file)