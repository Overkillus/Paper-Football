import sys
import pygame

pygame.init()
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
box = pygame.Rect(10, 50, 50, 50)

while True:
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.type == pygame.K_q:
            sys.exit(0)

    # Update

    # box.x = (box.x + 1) % screenWidth
    # box.y = (box.y + 1) % screenHeight

    # box.x = pygame.mouse.get_pos()[0]
    # box.y = pygame.mouse.get_pos()[1]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        box.y = (box.y - 1) % screenHeight
    if keys[pygame.K_a]:
        box.x = (box.x - 1) % screenWidth
    if keys[pygame.K_s]:
        box.y = (box.y + 1) % screenHeight
    if keys[pygame.K_d]:
        box.x = (box.x + 1) % screenWidth

    # Drawing
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (200, 0, 0), box)
    pygame.display.flip()
