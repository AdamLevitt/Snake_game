import pygame
from pygame.math import Vector2
import sys
import random
import os

pygame.init()
pygame.display.set_caption("SNAKE")
pygame.font.init()
pygame.mixer.init()

BLOCK_SIZE = 40
NUM_CELLS = 20
WIDTH, HEIGHT = BLOCK_SIZE * NUM_CELLS, BLOCK_SIZE * NUM_CELLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60
INITIAL_SIZE = 4
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
MAX_SPEED = 50

FRUIT_SOUND = pygame.mixer.Sound(os.path.join("assets", "mixkit-extra-bonus-in-a-video-game-2045.wav"))
LOSE_SOUND = pygame.mixer.Sound(os.path.join("assets", "mixkit-player-losing-or-failing-2042.wav"))

COLOR_1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
COLOR_2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
COLOR_3 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
COLOR_4 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
COLOR_5 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
COLOR_6 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

SCORE_FONT = pygame.font.SysFont("comicsans", 25)

speed = 150
level = 1
TIMER = pygame.USEREVENT + 1
HIT = pygame.USEREVENT + 2
pygame.time.set_timer(TIMER, speed)


class FRUIT:
    """Class that initilaizes, assigns position randomly and displays fruits"""

    def __init__(self, list_check):
        """initilaize the FRUIT objects"""
        self.x = random.randint(0, NUM_CELLS - 1)
        self.y = random.randint(1, NUM_CELLS - 1)
        self.position = Vector2(self.x, self.y)
        self.list_check = list_check

        # Ensure that we are not creating fruits where the snake already exists
        while self.position in self.list_check:
            self.x = random.randint(0, NUM_CELLS - 1)
            self.y = random.randint(1, NUM_CELLS - 1)
            self.position = Vector2(self.x, self.y)

    def draw_fruit(self):
        """display fruits"""
        fruit_rect = pygame.Rect(int(self.position.x * BLOCK_SIZE), int(self.position.y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(WINDOW, GREEN, fruit_rect)


class SNAKE:
    """class to handle the snake"""

    def __init__(self):
        """initialize snake"""
        self.snake_list = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.dir = Vector2(-1, 0)
        self.length = len(self.snake_list)

    def draw_snake(self):
        """display th snake"""
        for ind, square in enumerate(self.snake_list):
            snake_rect = pygame.Rect(int(square.x * BLOCK_SIZE), int(square.y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)

            # Allow for colors to be displayed randomly based on length of snake
            if ind <= 10:
                pygame.draw.rect(WINDOW, BLUE, snake_rect)
            elif ind <= 20:
                pygame.draw.rect(WINDOW, COLOR_1, snake_rect)
            elif ind <= 30:
                pygame.draw.rect(WINDOW, COLOR_2, snake_rect)
            elif ind <= 40:
                pygame.draw.rect(WINDOW, COLOR_3, snake_rect)
            elif ind <= 50:
                pygame.draw.rect(WINDOW, COLOR_4, snake_rect)
            elif ind <= 60:
                pygame.draw.rect(WINDOW, COLOR_5, snake_rect)
            else:
                pygame.draw.rect(WINDOW, COLOR_6, snake_rect)

    def move(self):
        """Handle the snake movement"""
        copy_move = self.snake_list[:-1]  # remove last component in list
        new_snake_head = copy_move[0] + self.dir  # create the new sanke head

        # allow for snake to jump between opposite edges of the screen
        if new_snake_head.x == -1.0:
            new_snake_head += Vector2(20, 0)

        if new_snake_head.x == 20.0:
            new_snake_head -= Vector2(20, 0)

        if new_snake_head.y == 0.0:
            new_snake_head += Vector2(0, 19)

        if new_snake_head.y == 20.0:
            new_snake_head -= Vector2(0, 19)

        # if 'new' snake head is going to collide with snake body - post event HIT
        if new_snake_head in copy_move:
            pygame.event.post(pygame.event.Event(HIT))

        # Add new snake head to body and assign to self.snake_list
        copy_move.insert(0, new_snake_head)
        self.snake_list = copy_move[:]

    def snake_grow(self):
        """Grow snake"""
        end_1 = self.snake_list[-1]
        self.snake_list.insert(-1, end_1)
        self.length += 1


def display_board(score, level):
    """displays the board, Score and Level"""

    WINDOW.fill(BLACK)
    for across in range(0, WIDTH, BLOCK_SIZE):
        for down in range(BLOCK_SIZE, HEIGHT, BLOCK_SIZE):
            rectangle = pygame.Rect(across, down, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WINDOW, WHITE, rectangle, 1)
    score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)
    level_text = SCORE_FONT.render("Speed Level: " + str(level), 1, WHITE)
    WINDOW.blit(score_text, (WIDTH - score_text.get_width() - 10, 2))
    WINDOW.blit(level_text, (10, 2))


def main():
    run = True
    clock = pygame.time.Clock()
    score = 0
    global speed
    global level

    snake = SNAKE()
    fruit = FRUIT(snake.snake_list)

    while run:
        clock.tick(FPS)
        display_board(score, level)

        # Situation where snake eats fruit
        if fruit.position in snake.snake_list:
            FRUIT_SOUND.play()
            fruit = FRUIT(snake.snake_list)
            score += 1
            snake.snake_grow()

            # Increase snake speed at some interval of growth
            if score % 5 == 0:
                if speed > MAX_SPEED:
                    speed -= 10
                    pygame.time.set_timer(TIMER, 0)
                    pygame.time.set_timer(TIMER, speed)

                    level += 1
                else:
                    level = "Max Speed"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            # Move based on Timer event
            if event.type == TIMER:
                snake.move()

            if event.type == HIT:
                LOSE_SOUND.play()
                run = False
                level = 0
                speed = 150
                pygame.time.set_timer(TIMER, 0)
                pygame.time.set_timer(TIMER, speed)
                break

            # Change direction basedon keys pressed and ensure cannot go in opposite direction
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

    level = 0
    speed = 150
    main()


if __name__ == "__main__":
    main()
