# Snake Solving Algorithms
The classic game snake and various algorithms to play the game. This is not an AI.

## Installation
You need to have [Python](https://www.python.org/downloads/) and pip running.
Also, pygame is required.
```bash
pip install pygame
```

## Concept
The snake makes decisions staring from its head, since it´s moving from there


## Play the Game
In the directory of the repository execute
```bash
py game.py <number>
```
on Windows.
It should work the same on any OS, but hasn´t been tested.

The ```<number>``` attribute determines which algorithm will be used to play snake.

The window can be resized even while the game is running which resets the progress.

All results of each algorithm are saved in a file.

The game speed can be controlled using a scrolling mechanism like a ```mouse wheel``` or a ```touchpad```. Time can be frozen and unfrozen using the ```space key```. Additionally, the keys ```1```, ```2```, ```3``` can set the speed to fixed values quickly.


## Algorithms

| **number** |                                                                                        **Algorithm**                                                                                        |
|:----------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|      0     | **Manual Gameplay:** The player controls the snake using the arrow keys.                                                                                                                    |
|      1     | **Straight:** The snake is going straight for the food without knowing the position of its body.                                                                                            |
|      2     | **Turning:** The snake knows how to turn when its own body is in the way.                                                                                                                   |
|      3     | **Smart:** The snake doesn't die to the edge or itself.                                                                                                                                     |
|      4     | **Perfect:** It's not but is makes sure that at every time 80% of the free tiles are available to the head. The snake will trap itself on one side of the grid and cycles until it's dead. |
|      5     | **Gap:** This algorithm leaves a gap to avoid trapping itself, but it's not perfect.                                                                                                        |
|      6     | **Hamiltonian Cycle:** It lays out a path and follows it all the time. Will reach 100% but takes very long.                                                                                |
|      7     | **Skip of Hamiltonian Cycle:** The attempt to let the snake skip some parts of the Hamiltonian cycle, but it didn't work out.                                                               |
