import sys
import pygame

import Colours
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

# -------------------------------------------------------------------------------------------------------
class MenuUI:
    """
    Class representing menu view
    """
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

    # TODO find a place for those
    sound_rect = sound_icon.get_rect(topleft=(75, 430))
    settings_rect = settings_icon.get_rect(topleft=(15, 430))
    button_w = 100
    button_h = 40
    button_y = 150
    button_x = 230
    button_1 = pygame.Rect(button_x, button_y, button_w, button_h)
    button_2 = pygame.Rect(button_x + 140, button_y, button_w, button_h)
    # Delta time variables
    clock = pygame.time.Clock()
    delta_time = 0

    def __init__(self):
        # Initiating sound
        if not Settings.sound_muted:
            mixer.music.play(-1)
            mixer.music.set_volume(Settings.sound_volume)

    def main(self):
        global delta_time
        while True:
            self.event_handler()
            # Ticking
            delta_time += self.clock.tick() / 1000.0
            while delta_time > 1 / Settings.max_tps:
                delta_time -= 1 / Settings.max_tps
                self.update()
                self.render()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.type == pygame.K_q:
                sys.exit(0)
            # Mouse click
            elif event.type == pygame.MOUSEBUTTONUP:
                # Mouse click details
                click = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                # Toggle mute
                if sound_rect.collidepoint(mouse_pos) and click[0] and Settings.sound_muted:
                    Settings.sound_muted = False
                    mixer.music.unpause()
                elif sound_rect.collidepoint(mouse_pos) and click[0] and not Settings.sound_muted:
                    Settings.sound_muted = True
                    mixer.music.pause()
        # TEMP TODO
        click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if self.button_2.collidepoint(mouse_pos):
            screen.blit(button2_glow, (365, 145))
            if self.button_2.collidepoint(mouse_pos) and click[0] == 1:
                sys.exit(0)

        elif self.button_1.collidepoint(mouse_pos):
            screen.blit(button1_glow, (225, 145))
            if self.button_1.collidepoint(mouse_pos) and click[0] == 1:
                Game.main()
        else:
            pygame.draw.rect(screen, Colours.CYAN, self.button_1)
            draw_text('START', font, Colours.WHITE, screen, self.button_1.x + 18, self.button_1.y + 10)

    def update(self):
        mixer.music.set_volume(Settings.sound_volume)

    def render(self):
        # Clear screen
        screen.fill((0, 0, 0))
        # Background
        screen.blit(background, (0, 0))
        # Title
        screen.blit(title, (screen.get_width() / 2 - 140, 20))
        # Settings
        screen.blit(settings_icon, (15, 430))
        # Mute toggle
        if Settings.sound_muted:
            screen.blit(sound_icon_off, (75, 430))
        else:
            screen.blit(sound_icon, (75, 430))
        # Start and Exit buttons
        pygame.draw.rect(screen, Colours.CYAN, self.button_1)
        pygame.draw.rect(screen, Colours.PINK, self.button_2)
        draw_text('START', font, Colours.WHITE, screen, self.button_1.x + 18, self.button_1.y + 10)
        draw_text('QUIT', font, Colours.WHITE, screen, self.button_2.x + 25, self.button_2.y + 10)

        # Show new frame
        pygame.display.flip()

    def __draw_text(self, text, font, color, surface, x, y):
        text_object = font.render(text, 1, color)
        text_rect = text_object.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_object, text_rect)

# -------------------------------------------------------------------------------------------------------



# getting the x,y of the icon placed at specific coordinates
sound_rect = sound_icon.get_rect(topleft=(75, 430))
settings_rect = settings_icon.get_rect(topleft=(15, 430))




button_w = 100
button_h = 40
button_y = 150
button_x = 230

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
        click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.type == pygame.K_q:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                # Mute toggle
                if sound_rect.collidepoint(mouse_pos) and click[0] and Settings.sound_muted:
                    Settings.sound_muted = False
                    mixer.music.unpause()
                elif sound_rect.collidepoint(mouse_pos) and click[0] and not Settings.sound_muted:
                    Settings.sound_muted = True
                    mixer.music.pause()



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

        pygame.draw.rect(screen, Colours.CYAN, button_1)
        pygame.draw.rect(screen, Colours.PINK, button_2)

        draw_text('START', font, Colours.WHITE, screen, button_1.x + 18, button_1.y + 10)
        draw_text('QUIT', font, Colours.WHITE, screen, button_2.x + 25, button_2.y + 10)

        if button_2.collidepoint(mouse_pos):
            screen.blit(button2_glow, (365, 145))
            if button_2.collidepoint(mouse_pos) and click[0] == 1:
                sys.exit(0)

        elif button_1.collidepoint(mouse_pos):
            screen.blit(button1_glow, (225, 145))
            if button_1.collidepoint(mouse_pos) and click[0] == 1:
                Game.main()
        else:
            pygame.draw.rect(screen, Colours.CYAN, button_1)
            draw_text('START', font, Colours.WHITE, screen, button_1.x + 18, button_1.y + 10)


        pygame.display.update()
        # Game.clock.tick(60)
