#!/usr/bin/python3

import pygame

from snake import Snake
from exceptions import GameOver
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

    grid = Grid(width=50, height=30)
    graph.window_width = grid.width * graph.grid_size
    graph.window_height = grid.height * graph.grid_size

    robo_snakes = [Snake.random_robot_snake(grid, graph.SILVER)
                   for x in range(2)]
    for snake in robo_snakes:
        snake.speed = 5
    homo_snake = Snake.random_snake(grid, graph.GREEN)

    food = Food.random_food(grid)

    graph.init_screen()

    done = False

    while not done:

        try:
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

            for i in range(len(robo_snakes)):
                if robo_snakes[i].dead:
                    del robo_snakes[i]
                    snake = Snake.random_robot_snake(grid, graph.SILVER)
                    snake.speed = 5
                    robo_snakes.append(snake)
            if homo_snake.dead:
                homo_snake = Snake.random_snake(grid, graph.GREEN)
            if food.eaten:
                food = Food.random_food(grid)
                for snake in robo_snakes:
                    snake.detect_direction()

            clock.tick(50)
        except GameOver as go:
            print(go)
            done = True

    print("Snakes dead: {}, Food eaten: {}, Food - Snakes = {}".format(
        Snake.dead, Food.Food_eaten, Food.Food_eaten - Snake.dead))

    pygame.quit()

    print("Finished")


if __name__ == '__main__':
    main()
