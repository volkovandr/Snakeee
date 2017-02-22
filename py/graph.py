#!/usr/bin/python3

import pygame
from snake import Snake
window_height = 800
window_width = 1400

grid_size = 25
segment_radius = 20

secreen = None

BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTGREY = (192, 192, 192)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SILVER = (95, 158, 160)


def init_screen():
    global screen
    screen = pygame.display.set_mode((int(window_width), int(window_height)))
    pygame.display.set_caption("Snakeee")


def draw_grid():
    screen.fill(BLUE)
    for line_no in range(int(window_height / grid_size)):
        pygame.draw.line(
            screen, LIGHTGREY,
            (0, line_no * grid_size),
            (window_width, line_no * grid_size))
    for line_no in range(int(window_width / grid_size)):
        pygame.draw.line(
            screen, LIGHTGREY,
            (line_no * grid_size, 0),
            (line_no * grid_size, window_height))


def draw_snake(snake, frame_position):
    snake_color = snake.color if not snake.dead else YELLOW

    def draw_tail(circle_position, direction, snake_color, segment_radius):
        pygame.draw.circle(screen, snake_color, circle_position,
                           segment_radius, 0)
        pygame.draw.line(
            screen, RED,
            (circle_position[0] - 3 * Snake.deltas[direction][0],
             circle_position[1] - 3 * Snake.deltas[direction][1]),
            (circle_position[0] + 3 * Snake.deltas[direction][0],
             circle_position[1] + 3 * Snake.deltas[direction][1]))

    def draw_segment(circle_position, direction, snake_color, segment_radius):
        pygame.draw.circle(screen, snake_color, circle_position,
                           segment_radius, 0)
        pygame.draw.line(screen, RED,
                         (circle_position[0] - 3, circle_position[1]),
                         (circle_position[0] + 3, circle_position[1]))
        pygame.draw.line(screen, RED,
                         (circle_position[0], circle_position[1] - 3),
                         (circle_position[0], circle_position[1] + 3))

    def draw_head(circle_position, direction, snake_color, segment_radius):
        pygame.draw.circle(screen, snake_color, circle_position,
                           segment_radius, 0)

    segment_no = 0
    for segment in snake.segments:
        (x, y, direction) = segment
        if snake.dead:
            circle_position = (int(x * grid_size + grid_size / 2),
                               int(y * grid_size + grid_size / 2))
        else:
            circle_position = (
                int(x * grid_size + grid_size / 2 +
                    Snake.deltas[direction][0] * (frame_position - 1) *
                    grid_size),
                int(y * grid_size + grid_size / 2 +
                    Snake.deltas[direction][1] * (frame_position - 1) *
                    grid_size))
        if segment_no == 0:
            draw_func = draw_tail
        elif segment_no == len(snake.segments) - 1:
            draw_func = draw_head
        else:
            draw_func = draw_segment
        draw_func(circle_position, direction, snake_color, int(
            segment_radius * (0.75 + 0.25 * segment_no / len(snake.segments))))
        segment_no += 1


def draw_food(food):
    circle_position = (int(food.x * grid_size + grid_size / 2),
                       int(food.y * grid_size + grid_size / 2))
    pygame.draw.circle(screen, RED, circle_position, segment_radius, 0)
    pygame.draw.circle(screen, YELLOW, circle_position, 6, 0)
    pygame.draw.circle(screen, GREEN, circle_position, 3, 0)
