import sys

import pygame

import Game

bg = pygame.image.load("Art/Neon_theme1.png").convert_alpha()
bg = pygame.transform.scale(bg, (1280, 720))
screen = pygame.display.set_mode((Game.screenWidth, Game.screenHeight))
font = pygame.font.SysFont(None, 50)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    while True:
        Game.event_handler()
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()

        screen.blit(bg, (0, 0))
        # draw_text('main menu test', font, (255, 255, 255), screen, 600, 20)

        button_1 = pygame.Rect(40, 100, 200, 50)
        button_2 = pygame.Rect(1050, 100, 200, 50)
        # button_3 = pygame.Rect(50, 300, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (0, 255, 0), button_2)
        # pygame.draw.rect(screen, (0, 0, 255), button_3)
        draw_text('start', font, (0, 0, 0), screen, 100, 100)
        draw_text('exit', font, (0, 0, 0), screen, 1110, 100)
        if button_1.collidepoint(mouse) and click[0] == 1:
            Game.main()

        if button_2.collidepoint(mouse) and click[0] == 1:
            sys.exit(0)

        pygame.display.update()
        Game.clock.tick(60)


main_menu()
