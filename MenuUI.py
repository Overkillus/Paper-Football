import sys

import pygame

import Game

import tkinter as tk

bg = pygame.image.load("Art/Neon_theme1.png").convert_alpha()
bg = pygame.transform.scale(bg, (695, 500))
title = pygame.image.load("Art/paperTitle.png").convert_alpha()
title = pygame.transform.scale(title, (500, 80))
screen = pygame.display.set_mode((Game.screenWidth, Game.screenHeight))
font = pygame.font.SysFont("comicsansms", 20)


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
        screen.blit(title, (100, 0))
        # draw_text('main menu test', font, (255, 255, 255), screen, 600, 20)

        button_1 = pygame.Rect(40, 80, 80, 30)
        button_2 = pygame.Rect(40, 130, 80, 30)
        button_3 = pygame.Rect(570, 80, 80, 30)
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (0, 255, 0), button_2)
        pygame.draw.rect(screen, (0, 0, 255), button_3)
        draw_text('Start', font, (0, 0, 0), screen, button_1.x+10, button_1.y)
        draw_text('Exit', font, (0, 0, 0), screen, button_2.x+10, button_2.y)
        draw_text('options', font, (0, 0, 0), screen, button_3.x+10, button_3.y)
        if button_1.collidepoint(mouse) and click[0] == 1:
            Game.main()

        if button_2.collidepoint(mouse) and click[0] == 1:
            sys.exit(0)

        pygame.display.update()
        Game.clock.tick(60)


main_menu()
