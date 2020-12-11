import sys
import pygame
import Game
from pygame import mixer

import tkinter as tk  # tkinter is used for GUI. Probably will have to use it at some point for any input

import Settings

# Art
background = pygame.image.load("Art/lobby3_bg.png")
background = pygame.transform.scale(background, (Settings.screen_width, Settings.screen_height))
title = pygame.image.load("Art/logo_small.png")
# title = pygame.transform.scale(title, (250, 80))
settings_icon = pygame.image.load("Art/settings.png")  # TODO implement functionality to adjust various settings
sound_icon = pygame.image.load("Art/sound.png")
sound_icon_off = pygame.image.load("Art/sound_off.png")
button1_glow = pygame.image.load("Art/start_glow.png")
button2_glow = pygame.image.load("Art/quit_glow.png")
screen = pygame.display.set_mode((Game.screenWidth, Game.screenHeight))
font = pygame.font.SysFont("arialbold", 30)

# Sound
mixer.music.load('Sound/background.wav')


class MenuUI:
    def __init__(self):
        True

    def main(self):
        True

    def even_handler(self):
        True

    def update(self):
        True

    def render(self):
        True





# getting the x,y of the icon placed at specific coordinates
sound_rect = sound_icon.get_rect(topleft=(75, 430))
settings_rect = settings_icon.get_rect(topleft=(15, 430))



# Background music

# sound_on = True


button_w = 100
button_h = 40
button_y = 150
button_x = 230
CYAN = (5, 185, 242)
PINK = (255, 0, 208)
GREEN = (13, 255, 0)
WHITE = (255, 255, 255)

if not Settings.sound_muted:
    mixer.music.play(-1)
    mixer.music.set_volume(Settings.sound_volume)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():

    while True:
        # Game.event_handler()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.type == pygame.K_q:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                if sound_rect.collidepoint(mouse_pos) and click[0] and Settings.sound_muted:
                    Settings.sound_muted = False
                    mixer.music.unpause()

                elif sound_rect.collidepoint(mouse_pos) and click[0] and not Settings.sound_muted:
                    Settings.sound_muted = True
                    mixer.music.pause()

        click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))
        screen.blit(title, (screen.get_width() / 2 - 140, 20))
        screen.blit(settings_icon, (15, 430))

        if Settings.sound_muted:
            screen.blit(sound_icon_off, (75, 430))
        else:
            screen.blit(sound_icon, (75, 430))

        # draw_text('main menu test', font, (255, 255, 255), screen, 600, 20)

        button_1 = pygame.Rect(button_x, button_y, button_w, button_h)
        button_2 = pygame.Rect(button_x + 140, button_y, button_w, button_h)

        pygame.draw.rect(screen, CYAN, button_1)
        pygame.draw.rect(screen, PINK, button_2)

        draw_text('START', font, WHITE, screen, button_1.x + 18, button_1.y + 10)
        draw_text('QUIT', font, WHITE, screen, button_2.x + 25, button_2.y + 10)

        if button_2.collidepoint(mouse_pos):
            screen.blit(button2_glow, (365, 145))
            if button_2.collidepoint(mouse_pos) and click[0] == 1:
                sys.exit(0)

        elif button_1.collidepoint(mouse_pos):
            screen.blit(button1_glow, (225, 145))
            if button_1.collidepoint(mouse_pos) and click[0] == 1:
                Game.main()
        else:
            pygame.draw.rect(screen, CYAN, button_1)
            draw_text('START', font, WHITE, screen, button_1.x + 18, button_1.y + 10)







        pygame.display.update()
        Game.clock.tick(60)


main_menu()
