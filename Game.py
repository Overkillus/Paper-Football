import sys
import pygame

# Init
pygame.init()

# Screen variables
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Delta time variables
clock = pygame.time.Clock()
max_tps = 150.0  # temp: should be 20-30
delta_time = 0

# Entity variables
box = pygame.Rect(10, 50, 50, 50)
box_speed = 4


def main():
    global delta_time
    while True:
        event_handler()

        # Ticking
        delta_time += clock.tick()/1000.0
        while delta_time > 1/max_tps:
            delta_time -= 1/max_tps
            update()
        render()


def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.type == pygame.K_q:
            sys.exit(0)


def update():
    # Auto movement test
    # box.x = (box.x + 1) % screenWidth
    # box.y = (box.y + 1) % screenHeight

    # Mouse cursor movement test
    # box.x = pygame.mouse.get_pos()[0]
    # box.y = pygame.mouse.get_pos()[1]

    # WASD movement test
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        box.y = (box.y - box_speed) % screenHeight
    if keys[pygame.K_a]:
        box.x = (box.x - box_speed) % screenWidth
    if keys[pygame.K_s]:
        box.y = (box.y + box_speed) % screenHeight
    if keys[pygame.K_d]:
        box.x = (box.x + box_speed) % screenWidth


def render():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (200, 0, 0), box)
    pygame.display.flip()


main()
