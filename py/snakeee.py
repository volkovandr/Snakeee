#!/usr/bin/python3

import pygame

from snake import Snake
from grid import Grid
from food import Food
import graph


direction_key_map = {
    pygame.K_RIGHT: Snake.RIGHT,
    pygame.K_LEFT: Snake.LEFT,
    pygame.K_DOWN: Snake.DOWN,
    pygame.K_UP: Snake.UP}


def main():
    pygame.init()

    clock = pygame.time.Clock()

    grid = Grid(width=30, height=30)
    graph.window_width = grid.width * graph.grid_size
    graph.window_height = grid.height * graph.grid_size

    robo_snake = Snake.random_robot_snake(grid, graph.SILVER)
    Snake.random_robot_snake(grid, graph.SILVER)
    Snake.random_robot_snake(grid, graph.SILVER)
    Snake.random_robot_snake(grid, graph.SILVER)
    Snake.random_robot_snake(grid, graph.SILVER)
    Snake.random_robot_snake(grid, graph.SILVER)
    robo_snake.speed = 7
    homo_snake = Snake.random_snake(grid, graph.GREEN)

    food = Food.random_food(grid)

    graph.init_screen()

    done = False

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Close clicked!")
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in direction_key_map:
                    homo_snake.set_direction(direction_key_map[event.key])

        grid.move()
        grid.draw()
        pygame.display.flip()

        if robo_snake.dead:
            robo_snake = Snake.random_robot_snake(grid, graph.SILVER)
            robo_snake.speed = 7
        if homo_snake.dead:
            homo_snake = Snake.random_snake(grid, graph.GREEN)
        if food.eaten:
            food = Food.random_food(grid)
            robo_snake.detect_direction()

        clock.tick(50)

    pygame.quit()

    print("Finished")


if __name__ == '__main__':
    main()
