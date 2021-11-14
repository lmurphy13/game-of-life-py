# John Conway's Game of Life

Conway's Game of Life is a zero-player game that employs cellular automata. The rules are very simple:
* A live cell dies from lonliness if it has less than two neighbors
* A live cell dies from overcrowding if it has more than three neighbors
* A live cell continues to the next generation if it has two or three neighbors
* A cell is born if it has exactly three neighbors

## Requirements
* Python3 with the Tkinter library

## Usage
To run this program, execute either
```
python3 gameoflife.py
```
or
```
./gameoflife.py
```

A number of "worlds" are provided with this app. Click File, Import World and choose a world from the `worlds` directory. 
You can save a current world by selecting File, Export World. 

The Start and Stop buttons will start and stop the game. Step will calculate one generation at a time. Reset will clear the world.

You can click on a cell to toggle it being alive or dead.

You can select the speed of the animation using the Speed slider.

## Note
The color options have not been implemented yet.
