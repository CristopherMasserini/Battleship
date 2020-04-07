# Battleship
## Overview
A project that can play a fully functional game of battleship. There is one game where two players can play against each other on a functional user interface.This project is done with Python 3.8.1

There are also files that are being used to set up a simulation of players playing the game battleship using different strategies. This is being done so that there can be an analysis on the effectiveness of different stratigies.

### Functionality
This file is where the ship and player classes are created as well as miscellaneous functionality for firing shots. 

The player class is subclassed by the automated player class which is used for the automated game option.

### Gui
Where the gui is set up for the interaction between two players playing the game. Keeps track of ships for each player and games won. Can quit or start a new game as well.

### Game
Where functionality and gui come together so the players can play the game.

### Strategy
Where all the strategies are coded for the automated players. Strategies so far are:
 - Random: The player fires randomly in the board
 - Blanket: The player starts at the top right corner and fires on the next box in the grid
 - Smart Random: Randomly fires until a ship is hit, than fires to destroy the ship
 - Smart Odd: Same as smart random, but the random firing is done on only the every other box, so there is less random firing to be done

### Automated Game
The functionality and strategy comes together so the automated players can play the game.

## Libraries
The GUI is done using tkinter and the testing with unittest. The project is done as a project to build experience and knowledge in python development. 

## Misc.
The project is laid out so that the game files are the only ones dependent on the files for functinality, strategies, and/or the gui, with the obvious exception of the test files. 
