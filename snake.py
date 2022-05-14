import pygame
from pygame.math import Vector2
import sys
import random
import os

pygame.init()
pygame.display.set_caption("SNAKE")

BLOCK_SIZE = 40
NUM_CELLS = 20
WIDTH, HEIGHT = BLOCK_SIZE * NUM_CELLS, BLOCK_SIZE * NUM_CELLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
FPS = 60
INITIAL_SIZE = 4
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

TIMER = pygame.USEREVENT
pygame.time.set_timer(TIMER, 250)


class FRUIT:
    def __init__(self):
        self.x = random.randint(0, NUM_CELLS - 1)
        self.y = random.randint(1, NUM_CELLS - 1)
        self.position = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.position.x * BLOCK_SIZE), int(self.position.y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(WINDOW, GREEN, fruit_rect)


class SNAKE:
    def __init__(self):
        self.snake = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.dir = Vector2(-1, 0)

    def draw_snake(self):
        for square in self.snake:
            snake_rect = pygame.Rect(int(square.x * BLOCK_SIZE), int(square.y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WINDOW, BLUE, snake_rect)

    def move(self):
        copy_move = self.snake[:-1]
        new_snake_head = copy_move[0] + self.dir

        if new_snake_head.x == -1.0:
            new_snake_head += Vector2(20, 0)

        if new_snake_head.x == 20.0:
            new_snake_head -= Vector2(20, 0)

        if new_snake_head.y == 0.0:
            new_snake_head += Vector2(0, 19)

        if new_snake_head.y == 20.0:
            new_snake_head -= Vector2(0, 19)

        copy_move.insert(0, new_snake_head)
        self.snake = copy_move[:]


def display_board():
    WINDOW.fill(BLACK)
    for across in range(0, WIDTH, BLOCK_SIZE):
        for down in range(BLOCK_SIZE, HEIGHT, BLOCK_SIZE):
            rectangle = pygame.Rect(across, down, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WINDOW, WHITE, rectangle, 1)


def main():
    run = True
    clock = pygame.time.Clock()
    snake = []

    fruit = FRUIT()
    snake = SNAKE()

    while run:
        clock.tick(FPS)
        display_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == TIMER:
                snake.move()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.dir != Vector2(0, 1):
                    snake.dir = Vector2(0, -1)

                if event.key == pygame.K_DOWN and snake.dir != Vector2(0, -1):
                    snake.dir = Vector2(0, 1)

                if event.key == pygame.K_LEFT and snake.dir != Vector2(1, 0):
                    snake.dir = Vector2(-1, 0)

                if event.key == pygame.K_RIGHT and snake.dir != Vector2(-1, 0):
                    snake.dir = Vector2(1, 0)

        fruit.draw_fruit()
        snake.draw_snake()
        pygame.display.update()


if __name__ == "__main__":
    main()
