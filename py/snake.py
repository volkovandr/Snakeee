#!/usr/bin/python3
'''
Implementation of the Snake class responsible for movement of the Snake
'''

from time import time
from food import Food
from random import randint
from copy import deepcopy
from exceptions import GameOver


class Snake:

    dead = 0
    default_speed = 3
    default_length = 10

    UP, DOWN, LEFT, RIGHT = 'UP', 'DOWN', 'LEFT', 'RIGHT'
    deltas = {
        UP: (0, -1),
        DOWN: (0, 1),
        LEFT: (-1, 0),
        RIGHT: (1, 0)
    }

    def random_snake(grid, color):
        if grid.borders_occupied():
            raise GameOver("GAME OVER: There is no free space at borders "
                           "to create a new snake")
        while True:
            side = [Snake.UP, Snake.DOWN, Snake.LEFT, Snake.RIGHT][
                randint(0, 3)]
            rand_x = randint(0, grid.width - 1)
            rand_y = randint(0, grid.height - 1)
            if side == Snake.UP:
                if not grid.occupied(rand_x, 0):
                    return Snake(
                        rand_x, -1, Snake.DOWN, Snake.default_length,
                        Snake.default_speed, grid, False, color)
            elif side == Snake.DOWN:
                if not grid.occupied(rand_x, grid.height - 1):
                    return Snake(
                        rand_x, grid.height, Snake.UP,
                        Snake.default_length, Snake.default_speed, grid,
                        False, color)
            elif side == Snake.LEFT:
                if not grid.occupied(0, rand_y):
                    return Snake(
                        -1, rand_y, Snake.RIGHT, Snake.default_length,
                        Snake.default_speed, grid, False, color)
            else:
                if not grid.occupied(grid.width - 1, rand_y):
                    return Snake(
                        grid.width, rand_y, Snake.LEFT,
                        Snake.default_length, Snake.default_speed, grid,
                        False, color)

    def random_robot_snake(grid, color):
        snake = Snake.random_snake(grid, color)
        snake.robot = True
        return snake

    def __init__(self, x, y, direction, length,
                 speed, grid, robot, color):
        self.segments = []
        self.head_x, self.head_y = x, y
        self.direction = direction
        self.new_direction = direction
        self.speed = speed
        self.framestart = None

        for seg_no in range(length):
            self.segments.append((x - Snake.deltas[direction][0] * seg_no,
                                  y - Snake.deltas[direction][1] * seg_no,
                                  direction))
        self.segments.reverse()
        self.direction_stack = []
        if grid:
            grid.add_object(self)
        self.grid = grid
        self.dead = False
        self.frame_position = 0
        self.extending = False
        self.robot = robot
        self.color = color

    def length(self):
        return len(self.segments)

    def set_direction(self, direction):
        if len(self.direction_stack) == 0:
            if ((self.direction == Snake.UP and direction == Snake.DOWN) or
                (self.direction == Snake.DOWN and direction == Snake.UP) or
                (self.direction == Snake.RIGHT and direction == Snake.LEFT) or
                (self.direction == Snake.LEFT and direction == Snake.RIGHT)):
                return
        self.direction_stack.append(direction)
        # print("Added new direction to the stack:", direction)

    def detect_direction(self):
        # print("Detecting new direction.")
        try:
            food = self.grid.find_food()
        except:
            print("No Food found. Continuing old direction")
            return
        self.direction_stack = []
        path = self.build_path(self.head_x, self.head_y, food.x, food.y)
        if not len(path) > 1:
            return
        if self.head_x > path[1][0]:
            return self.set_direction(Snake.LEFT)
        if self.head_x < path[1][0]:
            return self.set_direction(Snake.RIGHT)
        if self.head_y > path[1][1]:
            return self.set_direction(Snake.UP)
        if self.head_y < path[1][1]:
            return self.set_direction(Snake.DOWN)

    def eat_food(self, food):
        food.eaten = True
        self.grid.remove_object(food)
        self.extending = True
        Food.Food_eaten += 1
        print("{} food eaten!".format(Food.Food_eaten))

    def move(self):
        if self.dead:
            return

        if not self.framestart:
            self.framestart = time()
        self.frame_position = (time() - self.framestart) * self.speed
        if self.frame_position < 1:
            return

        # print("Movind the Snake. Old position:")
        # self.print()

        if len(self.direction_stack):
            self.direction = self.direction_stack[0]
            del self.direction_stack[0]

        self.head_x += Snake.deltas[self.direction][0]
        self.head_y += Snake.deltas[self.direction][1]

        if not self.grid.within_grid(self.head_x, self.head_y):
            return self.die("Out of the grid")

        object_at_new_head = self.grid.occupied(self.head_x, self.head_y)
        if object_at_new_head:
            if type(object_at_new_head) is Food:
                self.eat_food(object_at_new_head)
            else:
                return self.die('Collision with an obstacle of type {}'.format(
                    type(object_at_new_head).__name__))

        self.segments.append((self.head_x, self.head_y, self.direction))
        if self.extending:
            self.extending = False
        else:
            del self.segments[0]

        if self.robot:
            self.detect_direction()

        # print("Snake moved. New position:")
        # self.print()

        if self.frame_position > 1:
            self.framestart += 1 / self.speed
            self.move()

    def print(self):
        print([self.segments[i - 1] for i in range(len(self.segments), 0, -1)])

    def die(self, reason=None):
        self.frame_position = 0
        self.dead = True
        if reason:
            print("I'm dead for the reason: '{}'".format(reason))
        Snake.dead += 1
        print("{} snakes are dead so far".format(Snake.dead))

    def occupied(self, x, y):
        for segment in self.segments:
            if x == segment[0] and y == segment[1]:
                return True
        return False

    def build_path(self, start_x, start_y, end_x, end_y):
        # print("Trying to find a path from ({}, {}) to ({}, {})".format(
        #     start_x, start_y, end_x, end_y))
        if start_x < 0 or start_y < 0 or start_x >= self.grid.width or \
                start_y >= self.grid.height:
        #     print("The start position is out of the grid. Exiting")
            return []
        grid = deepcopy(self.grid.build2d())

        def mark_cell(cell, step, next_search_cells):
            x, y = cell
            typ = type(grid[x][y])
            if typ is Snake or typ is int:
                return False
            grid[x][y] = step
            next_search_cells.append((x, y))
            return True

        def adjancent_cells(cell, grid):
            x, y = cell
            if x > 0:
                yield (x - 1, y)
            if y > 0:
                yield (x, y - 1)
            if x < len(grid) - 1:
                yield (x + 1, y)
            if y < len(grid[0]) - 1:
                yield (x, y + 1)

        search_cells = [(start_x, start_y)]
        grid[start_x][start_y] = 0
        step = 1
        while True:
            next_search_cells = []
            for search_cell in search_cells:
                if search_cell[0] == end_x and search_cell[1] == end_y:
                    break
                for check_cell in adjancent_cells(search_cell, grid):
                    mark_cell(check_cell, step, next_search_cells)
            if not len(next_search_cells):
                break
            step += 1
            search_cells = next_search_cells

        # for row in range(len(grid[0])):
        #     print([column[row] for column in grid])

        if type(grid[end_x][end_y]) is not int:
        #     print("Could not find a path from ({}, {}) to ({}, {})".format(
        #         start_x, start_y, end_x, end_y))
            return []

        path = [(end_x, end_y)]
        while True:
            cur_pos = path[len(path) - 1]
            if cur_pos[0] == start_x and cur_pos[1] == start_y:
                break
            for check_cell in adjancent_cells(cur_pos, grid):
                cell = grid[check_cell[0]][check_cell[1]]
                if type(cell) is int:
                    if cell < grid[cur_pos[0]][cur_pos[1]]:
                        path.append(check_cell)
                        break
        path.reverse()
        # print("Found a path: {}".format(path))
        return path
