import pygame
from pygame.math import Vector2
import sys
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


class FRUIT:
    def __init__(self):
        self.x = 40
        self.y = 80
        self.position = Vector2(self.x,self.y)
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.position.x,self.position.y,BLOCK_SIZE,BLOCK_SIZE)
        pygame.draw.rect(WINDOW, GREEN, fruit_rect)



def display_board():
    WINDOW.fill(BLACK)
    for across in range(0, WIDTH, BLOCK_SIZE):
        for down in range(BLOCK_SIZE, HEIGHT, BLOCK_SIZE):
            rectangle = pygame.Rect(across, down, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WINDOW, WHITE, rectangle, 1)


def handle_snake(keys, snake):
    last_key = ""

    if keys[pygame.K_UP] and last_key != "down":
        last_key = "up"

    if keys[pygame.K_DOWN] and last_key != "up":
        last_key = "down"

    if keys[pygame.K_RIGHT] and last_key != "left":
        last_key = "right"

    if keys[pygame.K_LEFT] and last_key != "right":
        last_key = "left"


def main():
    run = True
    clock = pygame.time.Clock()
    snake = []

    fruit = FRUIT()

    # Initial Snake
    for squ in range(INITIAL_SIZE):
        square = pygame.Rect((WIDTH / 2) + BLOCK_SIZE, HEIGHT / 2, BLOCK_SIZE, BLOCK_SIZE)
        square.x -= squ * BLOCK_SIZE
        snake.append(square)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.quit()

        keys = pygame.key.get_pressed()
        handle_snake(keys, snake)
        print(snake)
        display_board()
        fruit.draw_fruit()
        pygame.display.update()




if __name__ == "__main__":
    main()
