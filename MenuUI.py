import sys

import pygame

import Game

import tkinter as tk #tkinter is used for GUI. Probably will have to use it at some point for any input

pygame.display.set_caption('Paper-Football')

bg = pygame.image.load("Art/lobby3_bg.png").convert_alpha()
#bg = pygame.transform.scale(bg, (695, 500))
title = pygame.image.load("Art/logo_small.png").convert_alpha()
#title = pygame.transform.scale(title, (500, 80))
settings_icon = pygame.image.load("Art/settings.png") #TODO implement functionality to adjust various settings
sound_icon = pygame.image.load("Art/sound.png") #TODO implement functionality to mute sound when clicked
screen = pygame.display.set_mode((Game.screenWidth, Game.screenHeight))
font = pygame.font.SysFont("arialbold", 30)

button_w = 100
button_h = 40
button_y = 150
button_x = 230
CYAN = (5,185, 242)
PINK = (255,0,208)
GREEN = (13,255,0)
WHITE = (255,255,255)



def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    while True:
        pygame.event.get()
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()

        screen.blit(bg, (0, 0))
        screen.blit(title, (screen.get_width()/2-140, 20))
        screen.blit(settings_icon,(15, 430))
        screen.blit(sound_icon,(75, 430))
        # draw_text('main menu test', font, (255, 255, 255), screen, 600, 20)

        button_1 = pygame.Rect(button_x, button_y, button_w, button_h)
        button_2 = pygame.Rect(button_x+140, button_y, button_w, button_h)

        pygame.draw.rect(screen, CYAN, button_1)
        pygame.draw.rect(screen, PINK, button_2)

        draw_text('START', font, WHITE, screen, button_1.x+18, button_1.y+10)
        draw_text('EXIT', font, WHITE, screen, button_2.x+25, button_2.y+10)

        if button_1.collidepoint(mouse) and click[0] == 1:
            Game.main()

        if button_2.collidepoint(mouse) and click[0] == 1:
            sys.exit(0)

        pygame.display.update()
        Game.clock.tick(60)


main_menu()
