import sys
import pygame

screen = pygame.display.set_mode((1280, 720))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
