## Program Details
Author: Kaushik Chatterjee (https://github.com/kchatr)
Date: 2021/03/30
Version: 1.19
Python 3.6.8 :: Anaconda, Inc.

## Description
This is a recreation of the classic (and infamous) Flappy Bird game in Python!
It was created using PyGame and uses the original sprites and assets in the game.
However, this time its not just a human playing the game - it's an AI.
Using the NEAT-Python library, I was able to create AI birds that continually train and evolve through generations.
Eventually, there is one bird that is invincible and this bird's neural network is pickled and saved.
The game hence has 3 modes: Play; Train; Learn
The user can either play the game, train their own invincible bird, or watch an unbeatable bird play the game and learn.

## Features
The development of the game followed the Object-Oriented Programming model.
All assets are subclasses of the Game interface, providing a standardized model that can be used for other games.
The bird, pipe, and ground are classes in their own right to make it easier to control their behaviour and features.
Finally, this is put together in a driver class which contains the different game modes.
The NEAT library was used to abstract the actual creation and implementation of the neural networks.
Using a generative algorithm, each bird is controlled by a random neural network as specified by the NEAT config file.
This allows for the training of birds without Deep Q-Learning, and makes each generation 'smarter'. 
The best bird's neural network is saved in a local file using Python's pickle library for objects.
All input and output is controlled in the PyGame window and handled with different screens.
The user can quit as well as restart the game, providing the most streamlined experience possible.

## Restrictions
The user cannot implement custom keybinds for actions and can only use the keyboard keys programmed.
Additionally, the user can't customize the bird or the background unless they wish to modify the source code.

## Known Errors
There are no known errors
