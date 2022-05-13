import pygame
import os

pygame.init()
pygame.display.set_caption('SNAKE')

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
BLOCK_SIZE = 40

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

def display():
    WINDOW.fill(BLACK)
    for across in range(0, WIDTH, BLOCK_SIZE):
        for down in range(0, HEIGHT, BLOCK_SIZE):
            rectangle = pygame.Rect(across,down, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WINDOW, WHITE, rectangle, 1)

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    snake = []

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        display()
        
    pygame.quit()

if __name__ == '__main__':
    main()



