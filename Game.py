import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
box = pygame.Rect(10, 50, 100, 100)

while True:
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    # Update
    box.x += 1
    box.y += 1

    # Drawing
    pygame.draw.rect(screen, (200, 0, 0), box)
    pygame.display.flip()
