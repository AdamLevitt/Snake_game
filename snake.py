from pickle import LIST
import pygame
from pygame.math import Vector2
import sys
import random
import os

pygame.init()
pygame.display.set_caption("SNAKE")
pygame.font.init()

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

SCORE_FONT = pygame.font.SysFont("comicsans", 25)

speed = 150
level = 1
TIMER = pygame.USEREVENT
pygame.time.set_timer(TIMER, speed)


class FRUIT:
    def __init__(self, list_check: LIST):
        self.x = random.randint(0, NUM_CELLS - 1)
        self.y = random.randint(1, NUM_CELLS - 1)
        self.position = Vector2(self.x, self.y)
        self.list_check = list_check

        while self.position in self.list_check:
            self.x = random.randint(0, NUM_CELLS - 1)
            self.y = random.randint(1, NUM_CELLS - 1)
            self.position = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.position.x * BLOCK_SIZE), int(self.position.y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(WINDOW, GREEN, fruit_rect)


class SNAKE:
    def __init__(self):
        self.snake_list = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.dir = Vector2(-1, 0)
        self.length = len(self.snake_list)

    def draw_snake(self):
        for square in self.snake_list:
            snake_rect = pygame.Rect(int(square.x * BLOCK_SIZE), int(square.y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WINDOW, BLUE, snake_rect)

    def move(self):
        copy_move = self.snake_list[:-1]
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
        self.snake_list = copy_move[:]

    def snake_grow(self):
        end_1 = self.snake_list[-1]
        self.snake_list.insert(-1, end_1)
        self.length += 1


def display_board(score):
    WINDOW.fill(BLACK)
    for across in range(0, WIDTH, BLOCK_SIZE):
        for down in range(BLOCK_SIZE, HEIGHT, BLOCK_SIZE):
            rectangle = pygame.Rect(across, down, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WINDOW, WHITE, rectangle, 1)
    score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)
    WINDOW.blit(score_text,(WIDTH - score_text.get_width() - 10, 2))


def main():
    run = True
    clock = pygame.time.Clock()
    score = 0
    global speed

    snake = SNAKE()
    fruit = FRUIT(snake.snake_list)

    while run:
        clock.tick(FPS)
        display_board(score)

        if fruit.position in snake.snake_list:
            fruit = FRUIT(snake.snake_list)
            score += 1
            snake.snake_grow()

            if score % 5 == 0:
                print('yes')
                speed -= 10
                pygame.time.set_timer(TIMER, 0)
                pygame.time.set_timer(TIMER, speed)

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
