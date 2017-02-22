#!/usr/bin/python3
'''
Implementation of the Food class
'''

from random import randint
from time import time
from exceptions import GameOver


class Food:

    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.eaten = False
        grid.add_object(self)

    def random_food(grid):
        start = time()
        while True:
            x = randint(1, grid.width - 2)
            y = randint(1, grid.height - 2)
            if not grid.occupied(x, y):
                return Food(x, y, grid)
            if time() - start > 10:
                raise GameOver("Cannot find a place for a new Food")
    Food_eaten = 0
