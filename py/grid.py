#!/usr/bin/python3
'''
Objects related to the World (grid)
'''
import graph
from snake import Snake
from food import Food


class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []
        self.grid = None

    def add_object(self, new_object):
        self.objects.append(new_object)

    def remove_object(self, old_object):
        for i in range(len(self.objects)):
            if self.objects[i] == old_object:
                del self.objects[i]
                return

    def within_grid(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        return True

    def move(self):
        for obj in self.objects:
            if type(obj) is Snake:
                obj.move()
        self.grid = None

    def draw(self):
        graph.draw_grid()
        for obj in self.objects:
            if type(obj) is Snake:
                graph.draw_snake(obj, obj.frame_position)
            elif type(obj) is Food:
                graph.draw_food(obj)

    def occupied(self, x, y):
        if not self.grid:
            self.build2d()
        return self.grid[x][y]

    def borders_occupied(self):
        for i in range(self.width):
            if not self.occupied(i, 0):
                return False
            if not self.occupied(i, self.height - 1):
                return False
        for i in range(self.height):
            if not self.occupied(0, i):
                return False
            if not self.occupied(self.width - 1, i):
                return False
        return True

    def build2d(self):
        if self.grid:
            return self.grid
        grid = [[None for i in range(self.height)] for i in range(self.width)]
        for obj in self.objects:
            if type(obj) is Snake:
                for segment in obj.segments:
                    if (segment[0] >= 0 and segment[0] < self.width and
                            segment[1] >= 0 and segment[1] < self.height):
                        grid[segment[0]][segment[1]] = obj
            if type(obj) is Food:
                grid[obj.x][obj.y] = obj
        self.grid = grid
        return self.grid

    def find_food(self):
        for obj in self.objects:
            if type(obj) is Food:
                return obj
        raise Exception("Food not found")
